# Building the keyword universe

The map is only as good as the demand behind it. This is how to get from one
seed to thousands of queries a real person typed, and how to spot when the
expansion has gone somewhere you did not intend.

## Contents

- [Why autocomplete](#why-autocomplete)
- [The four sources](#the-four-sources)
- [How the probes work](#how-the-probes-work)
- [Going deeper: a breadth-first search](#going-deeper-a-breadth-first-search)
- [Topics and demand mass](#topics-and-demand-mass)
- [Choosing the SERP sample](#choosing-the-serp-sample)
- [Drift, and the tokens that stop it](#drift-and-the-tokens-that-stop-it)
- [Locales and non-English seeds](#locales-and-non-english-seeds)
- [Flags worth knowing](#flags-worth-knowing)

## Why autocomplete

A suggestion list is not a guess about demand — it is a record of queries
people actually completed, served by the engine itself, free, and without an
API key. It gives you no volume number, and pretending otherwise would be the
one dishonest thing in this pipeline. What it does give you is shape: which
questions exist, how they are phrased, and how they branch. Volume is what
paid tools sell; shape is what decides what you write.

Where the skill needs a weight, it uses **demand mass** — how many keywords in
the universe cluster around a topic — and says so. That is a real, countable
quantity from this corpus, not a smuggled volume estimate.

## The four sources

| source | per call | extras | overlap with Google web |
|---|---|---|---|
| `google` (`client=chrome`) | 15 | relevance scores, suggest subtypes | — |
| `youtube` (`ds=yt`) | 10 | video-intent phrasing | ~50% — genuinely different |
| `ddg` | 8 | — | ~60% |
| `bing` | 13 | — | ~70% |

Default is `google` alone, and for most runs that is right. Add `youtube` when
the topic has a demonstrable or visual half — repairs, recipes, techniques,
software walkthroughs — because it surfaces "how to descale...", "...not
working" phrasings that web autocomplete ranks lower. `ddg` and `bing` mostly
return subsets of Google; use them to corroborate a surprising keyword rather
than to pad the list, and remember every extra source multiplies the call
count.

## How the probes work

Autocomplete completes a *prefix*, so every probe is the seed plus a shape, and
the shapes decide which half of the market you see:

```
seed                          espresso machine
question words + seed         how espresso machine, why espresso machine, ...
seed + commercial words       espresso machine best, espresso machine vs, ...
seed + relation words         espresso machine for, espresso machine with, ...
seed + a..z                   espresso machine a, espresso machine b, ...
```

Every shape is asked of **both forms of the seed**, singular and plural, so
"claude skill" also probes "claude skills". Autocomplete is literal: the two
are one topic to a reader and two different prefixes to the API. Seeded with
one form alone, a real run reached only 35% of the keywords the other found —
and every keyword the plural run found would have passed the singular run's own
guard, so the gap was never the filter, only which prefixes were ever asked.
Probing both raised layer 1 by 65% and met the same target in half the calls,
because breadth at layer 1 is inherited by every layer under it. Mass nouns are
left alone: there is no "softwares" to ask for.

Around 180 probes, and they are layer 1. The order matters: the plain seeds and
the modifier families run before the alphabet, and the form you actually typed
runs before its twin, so a run cut short still has the high-value shapes rather
than `seed a` through `seed f`.

## Going deeper: a breadth-first search

Completing the seed forever only ever returns the head of the market. Depth is
where the specific, low-competition tail lives, so keywords that came back get
re-probed in turn. The search is **breadth-first**: a layer is finished before
the next one starts.

```
layer 0   the seed
layer 1   completions of the seed through every probe shape   -- always expanded in full
layer 2   completions of every layer-1 keyword
layer 3   completions of every layer-2 keyword
...
```

That ordering is the point, not an implementation detail. A keyword two
completions from the seed is a different kind of query from one five
completions out — broader, higher-volume, more contested — and a search that
mixes layers explores neither properly. Going depth-first, or greedily by
score, produces a universe that is deep in a few phrasings and blind
everywhere else, and nothing in the output tells you which.

**Layer 1 is always expanded to exhaustion**, whatever `--branch` says. It is
the breadth every deeper layer inherits: leave one layer-1 node unprobed and
the entire subtree under it is missing from the universe with nothing to mark
that it ever existed. Layer 1 is small — tens to a low thousand nodes — so
completing it is cheap, and it is the only layer where completeness is worth
buying unconditionally.

Every layer below it is ranked, then expanded in waves of `--wave` nodes, and
allowed to stop where it stops paying (`--min-yield` new keywords per probe) or
at `--branch` nodes.

### The ranking

Deeper layers can be too large to exhaust, so the order matters — and "worth
expanding" is a different question from "good keyword". A long, highly specific
query can be an excellent keyword and a dead end as a probe, because there is
nothing left to append to it.

The score is **headroom, and nothing else**: how much room the query has left to
complete, measured in characters. It started as a five-part blend, which a real
run's own data then graded — every node records what expanding it actually
returned, so each ingredient could be correlated against realised yield over
2,044 expanded nodes:

| signal | weight it had | ρ vs. realised yield |
|---|---|---|
| relevance | 0.34 | **+0.01** — near-constant: 33 distinct values, half of them 600 or 601 |
| headroom | 0.21 | **+0.24** by words, **+0.33** by characters |
| corroboration | 0.16 | −0.03 |
| parentage | 0.15 | +0.17 |
| rank | 0.14 | −0.05 |
| *the blend* | — | **+0.10** — worse than headroom alone, by a factor of three |

Three dead signals carrying 64% of the weight were dragging the ranking below
what its best ingredient managed unaided. Characters beat words for the same
idea because they have four times the resolution — 50 distinct values against
12 — and ties fall back to the same ordering anyway.

Re-graded across seven seeds after the change, ρ runs +0.21 to +0.36 on topics
large enough for the order to matter, and the top score decile returns 3–9×
what the bottom decile returns. Two caveats worth keeping: on a small topic
every layer is exhausted anyway, so the ranking changes nothing there and its ρ
is correspondingly weak; and 30–60% of expanded nodes return nothing at all in
most corpora, so the honest prediction target is "any children at all" rather
than how many.

Ranked order alone would still dig one hole: the top 150 completions of one
seed are mostly one phrasing, and so are their completions. So the ranked
frontier is bucketed by each node's leading modifier and the buckets are
rotated through — best node from each, biggest bucket first. A layer expanded
to exhaustion ends up with the same set either way; this decides the order,
which is what matters when a deeper layer stops early.

### What the JSON records

`search.layers` carries one entry per layer, and it is the record that
distinguishes a small topic from an abandoned search:

```json
{"layer": 3, "from_layer": 2, "discovered": 872, "frontier": 264,
 "expanded": 264, "probes": 264, "policy": "ranked",
 "stopped_because": "layer exhausted", "seconds": 11.3}
```

`policy` is the rule the layer ran under (`exhaustive` for layer 1, `ranked`
below it); `stopped_because` is what actually happened, so a `ranked` layer
that ran out of frontier still reports `layer exhausted`.
`search.frontier_fully_explored` is true only when every layer ended that way.

Each keyword carries its own place in the tree: `level` (its layer), `probe`
(the query whose completion produced it), `rank` and `relevance` within that
suggestion list, plus `expanded`, `children_found` and `expansion_score`.

When the universe gets trimmed to `--target`, **layer 1 is kept whole** and
deeper layers keep a quota (roughly 35/25/20/15). Sorting by layer instead
would put every deep keyword last and a small target would silently throw away
the entire point of digging.

## Topics and demand mass

Each keyword is filed under its most-shared substantive word: "espresso machine
with grinder" and "does espresso machine come with grinder" both land under
`grinder`. Two guards make that useful:

- **Intent words cannot anchor a topic.** "best", "review", "2026", "reddit"
  describe *how* someone is searching, not what about. Without this guard half
  the universe files under "best" and the clustering tells you nothing.
- **A word used by more than `--df-ceiling` of the universe cannot anchor
  either.** For an "espresso machine" run, "coffee" appears in 8.7% of
  keywords; letting it anchor produced one 423-keyword cluster that meant
  nothing. At the 5% default the largest cluster is 3.6% of the corpus and 92%
  of keywords land in clusters of three or more.

Cluster size is the demand mass that later weights the dots on every 2x2.

This is wording-based grouping, and wording is a proxy for intent, not a
substitute. `serp_metrics.py` regroups the sampled keywords by the URLs Google
actually returns. Where the two disagree, Google wins.

## Choosing the SERP sample

One representative per topic, biggest topic first, then a second from each, and
so on. Spending searches this way spreads them across the demand instead of
piling ten of them on ten phrasings of one question. In a 4,891-keyword run a
120-keyword sample covered 119 distinct topics.

The seed itself is always in the sample. Each sampled keyword carries its
topic's size, so a dot on the map can be weighted by what stands behind it.

## Drift, and the tokens that stop it

Autocomplete walks away from your seed given half a chance: `how espresso
machine` completes to `how coffee machine`, and `a espresso machine` to `a
coffee machine game`. Left alone, a few hundred off-topic keywords enter the
universe and every downstream number is diluted.

The filter is a small set of tokens, and **every one of them has to survive**.
The set is the seed's own content words minus the category noun — the
`software`, `platform`, `tool`, `app`, `machine` half of the seed — capped at
three.

Dropping the category noun matters more than it looks. It is usually the
longest word in the seed and always the word searchers vary most freely —
autocomplete answers "cold email software" with "cold email tool", "cold email
platform", "cold email client" — so requiring it pins the universe to the one
token the market does not agree on. Requiring it discarded about three
quarters of that seed's real demand.

Requiring *all* of what is left, rather than any one, matters just as much. A
compound seed is usually compound because neither half names the topic alone:
"ai" and "harness" are each enormous and unrelated subjects, and a guard
satisfied by either fills the universe with dog leads, safety belts, wiring
looms and horse racing. On a real "ai harness" run that was 82% of the output.

Tokens are matched as words, and the length picks how loosely:

| token | matched as | so it catches | and not |
|---|---|---|---|
| `ai`, `ml`, `3d` (≤3 chars) | whole word | "harness for ai agents" | training, airtag, aircraft, airlift |
| `email`, `harness` (≥4) | word prefix | emailing, emails, harnesses | — |
| `"cold email"` (phrase) | phrase at a word start | "cold emailing" | — |

Short tokens have to be whole words in both directions. Plain substring lets
`ai` match *tr**ai**n* and *em**ail***; anchoring only the front still lets it
match *ai*rtag and *ai*rcraft, which is most of what an "ai harness" universe
fills up with otherwise.

The conjunction is capped at three tokens because past that it asks a real
query to repeat more of the seed than real queries do. "best claude skills for
data analysis" would demand claude AND skills AND data AND analysis, and drop
"claude skills for data science" for the last one.

Tighten with a phrase when a seed's meaning lives in the pair rather than
either word: `--must-include "cold email"`. Values are comma-separated and all
of them are required: `--must-include "claude,skills"`. Pass `--must-include -`
to keep everything, which is occasionally right for a very broad seed and
usually not.

**When one token is doing all the rejecting**, the run says so. A conjunction is
right when neither half of a compound seed names the topic alone ("ai harness"
is a dog lead without both) and wrong when one token already names it:
`cyanotype printing` demanding "printing" as well throws away "how cyanotype
works" and "what is a cyanotype", and returns 424 keywords where the topic noun
alone returns 5,000. Nothing lexical separates those two cases, so the expander
measures instead — it counts the suggestions each token is *solely* responsible
for rejecting, and when one token is doing most of it, names that token and the
`--must-include` value that frees it.

Dropped keywords are recorded with the reason in `keywords.json`. **When
`dropped_off_topic` is large relative to what was kept**, read the dropped list
before doing anything else — either the seed is ambiguous, or the filter is
wrong for it.

## Locales and non-English seeds

`--locale en-GB`, `--locale de-DE`, `--locale es-MX`. This sets `hl` and `gl`
on the autocomplete call, and both matter: a UK run returns different
suggestions and different spellings from a US one.

Two things to remember for non-English work. The stopword and intent lexicons
in `expand_keywords.py` are English, so `intent_prior` will mostly come back
`unclassified` — that costs you nothing, because intent is read from the SERP
later anyway and that step is language-independent. And keep the locale
consistent between expansion and search; a German keyword set scored against
US rankings is two datasets pretending to be one.

## Flags worth knowing

| Flag | Why |
|---|---|
| `--target N` | Universe size. 5,000 default; raise it freely, the calls are cheap |
| `--sample N` | Keywords marked for SERP capture. This one decides run length |
| `--depth N` | Deepest layer to reach, default 6. Layers stop early once `--target` is met or the frontier runs dry, so raising it costs nothing on a topic that is already exhausted. `--depth 1` is seed-only and fast |
| `--branch N` | Ceiling on nodes expanded in any one layer *below layer 1*, default 1500. Layer 1 is always expanded in full |
| `--wave N` | Nodes probed per wave inside a layer, default 150. Yield is measured per wave, so this is the granularity at which a layer can stop early |
| `--min-yield F` | New keywords per probe below which a layer below layer 1 stops, default 0.6. Lower it to keep digging a thin topic |
| `--sources` | `google,youtube` when the topic has a how-to half |
| `--locale` | Autocomplete is locale-specific; match it to the market |
| `--must-include` | The drift guard, comma-separated and all required. A phrase (`"cold email"`) tightens; fewer tokens, or `-`, widens |
| `--df-ceiling` | Lower it (0.03) if a near-synonym of the seed is swallowing topics |
| `--extra` / `--extra-file` | Keywords you found elsewhere — related searches, People Also Ask, the user's own list. Kept verbatim with `source: manual` |
| `--no-letters` | Skips the a-z round: ~25% fewer calls, noticeably less tail |

`--extra` is worth remembering. If the user hands you a list of keywords they
already care about, feed it in — those keywords join the universe, get
clustered and get sampled alongside everything discovered, instead of living in
a separate conversation.
