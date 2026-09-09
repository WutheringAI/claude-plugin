---
name: demand-validation
description: >-
  Test an idea against the cheapest evidence that could kill it — search demand, sustained
  ad spend, posted salaries, and the words buyers use — and return a verdict with the
  number that decides it. Use when: Before a build decision, when the question is whether
  the market exists at all. Use positioning-teardown instead if you already know the
  market exists and the question is who you are up against. Runs on Wuthering AI live data
  — about 13 billed calls, $2.60. Ask for a token first if there is none.
---

# Is there real demand for this?

**The job.** I have an idea. Tell me whether anyone is already paying to solve this, before I spend a quarter building it.

**The method.** Todd Jackson's four Ps and levels of product-market fit, with Bob Moesta's four forces used to explain why the demand exists rather than only that it does.

**Deliver.** A verdict — validated, refuted, or inconclusive — the single number that decides it, the two strongest pieces of evidence for, the strongest against, and the cheapest next call that would change your mind.

## Before you start

`$ARGUMENTS` is the product or idea to test, in one or two sentences. If it is empty, ask for it in one question and stop until you have it.

Then check the connection once:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --check
```

If that exits non-zero, run `/wuthering:connect` and stop until it succeeds. Every
call below spends the user's prepaid balance.

## Making the calls

One call is one command. The token is read from disk by the script, so it never
appears in this conversation:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/call.mjs" <tool> key=value key=value
```

Array values are comma-separated. `node "${CLAUDE_PLUGIN_ROOT}/scripts/call.mjs" --list`
prints every tool this deployment serves with its parameters; call nothing that
is not on that list.

**What this run costs.** About 13 billed calls, $2.60 at
20¢ per successful call. Stop at 24 ($4.80) — past
that you are confirming rather than learning. Failed calls are not charged. Say
the number out loud before a long run.

**Tools this method names.** `keyword_ideas`, `keyword_suggestions`, `domain_rankings`, `keyword_overview`, `keyword_volume`, `keyword_intent`, `ads_advertisers`, `ads_creatives`, `ads_meta_advertisers`, `ads_meta_library`, `web_search`, `company_jobs`, `social_reddit_posts`, `social_reddit_comments`, `app_reviews`, `keyword_history`

**Other inputs, if the user supplied them.** `audience` — Who it is for, if you have a view. A role and a company size is enough. `competitor` — One competitor domain you already know of. Saves the run its first two calls. `market` — Country to measure, if not the United States. Search demand varies sharply by country.

---

## The idea under test

<the idea, in one or two sentences>

## Before you spend a call

Write down the four Ps — Todd Jackson's frame for what you are actually
claiming. Doing this first is what makes the data falsifiable rather than
decorative, because each P names the evidence that would refute it.

  PERSONA  who specifically has this problem — a role, not a market
  PROBLEM  what they are doing today instead, and what it costs them
  PROMISE  the one outcome you would put on the homepage
  PRODUCT  the smallest thing that could deliver that promise

Then write the number that would make you walk away, before you know it. A
threshold chosen after the data arrives is not a threshold.

**THE EVIDENCE LADDER.** Rank every signal by what it would cost someone to
fake. Prefer signals higher up, and never let a lower rung outvote a higher one:

  1. Money      someone is paying a competitor, or sustaining ad spend
  2. Salary     a company is paying humans to do this job
  3. Search     commercial-intent queries with real, repeated volume
  4. Time       people build workarounds — spreadsheets, templates, macros
  5. Attention  views, engagement, followers, upvotes
  6. Words      someone said they would like it. Never sufficient on its own.

Rungs 1 and 2 cost money to fake. Rung 6 costs nothing, which is why so much
of it exists.

**FINDING URLS.** Several tools take a URL and cannot search for one
— `social_linkedin_posts`, `social_reddit_posts`, `social_reddit_comments`,
`company_jobs`, `company_person`, `web_fetch`. When you need a page, find its
URL with YOUR OWN web search first, using a site: filter. That costs nothing
and is exact. `web_search` does the same job for a billed call and is the
fallback when you have no search of your own. Never construct a URL from a company
name: a wrong URL comes back as a dead page, which reads as an absence of
evidence rather than as your mistake.

**BATCHING.** The keyword tools bill once per call however many
terms you send — `keyword_overview` takes 700, `keyword_volume` 1,000,
`keyword_intent` 1,000, `keyword_ideas` 200. Pool your terms and send them in one
call rather than looping. A batch whose rows exceed one response comes back
trimmed and says how many rows it held versus returned: size the next batch
from that figure and send the terms you did not get. A term missing from a
trimmed response was withheld, NOT measured at zero. Scoring it as zero is
the single most common way one of these runs reaches a confident wrong
answer.

**ONE CALL, NOT THREE.** `keyword_overview` returns volume, cost per click,
competition, difficulty, intent and the trend together, so it answers in one
billed call what `keyword_volume`, `keyword_intent` and `keyword_difficulty`
answer in three. Make it the scoring step for any list of 700 or fewer. The
other three keep their edges: a list longer than 700, and terms so new that no
index has seen them, which `keyword_volume` prices because it asks the ad
platform rather than reading a database. A term that comes back from
`keyword_overview` with no metrics is one of those — re-price that subset,
and never read the gap as zero demand.

## The method — cheapest killer first

### 1. Harvest the language. Do not invent keywords, find them.

- `keyword_ideas` on 3–5 seed terms taken from the PROBLEM, not from your
  product name. Buyers search their problem; only your existing customers
  search your category.
- `keyword_suggestions` on whichever seed came back richest, for the long
  specific phrases where intent lives.
- If you named a competitor: `domain_rankings` on their domain returns the
  terms they already win, which is the vocabulary of people who are already
  buying this.

Collect every candidate term. Do not price them yet, and do not filter them by
taste — the term you would never have written is the one worth finding.

### 2. Price the whole set in as few calls as it takes.

- `keyword_overview` on everything you harvested. Volume, cost per click and
  intent come back together, so the whole set is priced and classified in one
  call. Commercial and transactional intent with volume is demand.
  Informational volume alone is an audience, which is a different and much
  harder business.
- Past 700 terms, and for any term that came back without metrics, `keyword_volume`
  and `keyword_intent` cover the remainder.

**KILL CRITERION.** If the commercial-plus-transactional cluster totals under
~5,000 searches/month — or under ~1,000 for a B2B tool, where a buyer is worth
5–10× a consumer — stop here and say so. That is a real finding and it cost
you four calls. Report it as a finding, not as a failure to find something.

### 3. Look for money. This is the top rung, so reach it early.

- `ads_advertisers` on your two clearest competitor names or on the money
  terms themselves.
- `ads_creatives` on any advertiser it returns. Note `first_shown` and
  `last_shown` on every creative and compute the run length yourself.
- `ads_meta_advertisers` on a competitor's domain if the buyer is a consumer
  or a small business, where the spend goes to social rather than to search.
  It dates their Meta ads and hands back a `page_id`; `ads_meta_library` on
  that id renders the creatives.

A creative running 90+ days means their acquisition arithmetic works at that
message and that price. Nobody sustains a losing ad for a quarter. Note: in
the advertiser results the `title` field is the ADVERTISER NAME, not the ad
headline.

### 4. Look for salary. A posted band is what this problem is worth today.

- Find open roles with your own web search (`site:linkedin.com/jobs/view
  "<competitor>"`), or `web_search` if you have none.
- `company_jobs` on the two or three listings that look most revealing. Each
  call reads ONE listing, so choose rather than sweep.

Roles clustered on one function reveal the roadmap. A posted salary band is
the price of solving this problem with humans, which is the ceiling on what
software can charge for solving it without them.

### 5. Listen for the four forces.

Bob Moesta's frame: a switch happens when PUSH (frustration with today) plus
PULL (attraction to the new) beats ANXIETY (fear of switching) plus HABIT
(what they would have to stop doing). Most ideas die on anxiety and habit,
which is why "they said they loved it" and "they did not buy it" coexist so
often.

- Find where the buyer gathers with your own search, then
  `social_reddit_posts` on the threads, and `social_reddit_comments` on the
  one thread that is clearly the canonical complaint.
- `app_reviews` with `sort_by=most_recent` if a mobile competitor exists.
  Read the 1- and 2-star reviews first: a paying customer taking the time to
  complain is the strongest words-rung evidence there is.

Quote them verbatim. The exact phrasing is the finding — a paraphrase loses
the word the buyer would type into a search box.

### 6. Check the trend before concluding.

- `keyword_history` on your top 5 commercial terms.

Distinguish a durable shift from a spike. A rising term with no advertisers is
either early or worthless. Say which you think it is and why, and name what
would tell the two apart.

## The bar

Validated only when ALL of these hold. If one fails, say which:

- **Reach** — a commercial-intent cluster above ~5,000/mo, or ~1,000/mo B2B
- **Triangulation** — it survived a kill attempt from at least TWO independent
  families (search, ads, hiring, marketplace reviews, social)
- **Explanation** — the story of why this demand exists survived the data
- **Forces** — you can name the push and the pull, and you have a plan for the
  anxiety and the habit
- **Priced** — you have a CAC band from real CPCs, not a guess

"Promising" is not a verdict.

**RULES THAT MAKE THE OUTPUT TRUSTWORTHY**
- Cite the tool and the argument behind every number you state.
- Distinguish measured (a tool returned it) from inferred (you reasoned to it).
- State the strongest evidence AGAINST your conclusion before your conclusion.
- Absence of a signal is not evidence of absence. Name which instrument was
  blind and why.
- Coverage is public data and varies by query, country, and date. A thin
  result is a thin result, not an empty market.
- If the data does not settle it, say INCONCLUSIVE and name the one call that
  would settle it. An unspent budget and an uncertain answer at the same time
  is a failed run; so is a confident answer the data did not support.

## Deliver

The verdict. The one number that decides it. The two strongest pieces of
evidence for, and the strongest against, stated before your conclusion. Then
the single cheapest call that would change your mind — and make it a call this
API can actually serve.

---

The same method is served as text at https://wutheringai.com/v1/free/skills/demand-validation, free and
without a token, and explained for a person at https://wutheringai.com/skills/demand-validation.
