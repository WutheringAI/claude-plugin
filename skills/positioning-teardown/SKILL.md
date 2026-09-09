---
name: positioning-teardown
description: >-
  Work April Dunford's positioning sequence from public evidence: the alternatives a
  prospect would actually use, what only you do, the value that follows, who cares most,
  and the category that makes all of it obvious. Use when: Before a launch, a pricing page
  rewrite, or a sales-deck rebuild — and any time win rates are fine in the demo and bad
  in the deal. Use demand-validation instead if the market itself is still in question.
  Runs on Wuthering AI live data — about 15 billed calls, $3.00. Ask for a token first if
  there is none.
---

# Who are we really up against?

**The job.** Prospects do not understand why they would pick us. Tell me what they would do if we did not exist, and what makes us obviously the right choice for the ones who should buy.

**The method.** April Dunford's positioning components, in her order: competitive alternatives, unique attributes, value, best-fit customers, market category. Her test governs step 1 — if you did not exist, what would the prospect do? — and the status quo always counts as an alternative.

**Deliver.** A filled positioning statement — alternatives, unique attributes, value, best-fit customer, category — plus the competitor's tested claims, their untested ones, and the silence you can own.

## Before you start

`$ARGUMENTS` is your product, as a domain or a name and one sentence on what it does. If it is empty, ask for it in one question and stop until you have it.

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

**What this run costs.** About 15 billed calls, $3.00 at
20¢ per successful call. Stop at 27 ($5.40) — past
that you are confirming rather than learning. Failed calls are not charged. Say
the number out loud before a long run.

**Tools this method names.** `domain_rankings`, `domain_serp_rivals`, `domain_competitors`, `app_competitors`, `social_youtube_search`, `web_fetch`, `company_firmographics`, `company_funding`, `company_jobs`, `ads_advertisers`, `ads_creatives`, `ads_meta_advertisers`, `ads_meta_library`, `app_reviews`, `domain_top_pages`, `domain_keyword_overlap`, `keyword_overview`, `keyword_volume`, `keyword_intent`

**Other inputs, if the user supplied them.** `competitor` — A competitor domain to tear down first. Others are discovered from the data. `audience` — The segment you believe is your best fit, if you have a view. `market` — Country to measure, if not the United States.

---

## The product

<your product, and one sentence on what it does>

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

Work the five components in this order and do not skip ahead. April Dunford's
point is that the order is the method: the category you can credibly claim is
determined by your value, which is determined by your unique attributes, which
only mean anything relative to the alternatives. Teams that start at the
category end up naming one they cannot win.

## 1. COMPETITIVE ALTERNATIVES — what would they do if you did not exist?

Not "who is in our category". What a prospect would actually do on Monday
morning with the budget they have. Three kinds, and most teams only look for
the first:

- **Named products.** `domain_serp_rivals` on your five clearest money terms
  returns the domains that own those queries. `domain_competitors` on your own
  domain returns who overlaps you across your whole keyword set — often a
  different list, and the difference is instructive. `app_competitors` if the
  buying happens in a store.
- **Sustained advertisers.** `ads_advertisers` on the same terms. Someone
  paying every day to reach your buyer is an alternative whether or not you
  think of them as a competitor.
- **The status quo.** The spreadsheet, the agency, the intern, the manual
  process. Find it with `social_youtube_search` on "how to <the job>" and on
  "<the job> in excel" or "<the job> template" — a tutorial with six figures of
  views is a competitor with a marketing budget of zero and a monopoly on
  habit. Confirm the volume with `keyword_overview` on those phrases.

Write the alternatives list from the prospect's view. If the status quo is not
on it, you have not finished this step.

## 2. UNIQUE ATTRIBUTES — what do you have that they do not?

Attributes, not adjectives. Capabilities, data, integrations, a model, a
licence, a distribution position. Verify each against what the alternatives
actually ship:

- `web_fetch` their homepage, pricing page and one feature page as
  `format=markdown`. Use `format=html` when the detail sits in a table you
  need cell by cell.
- `company_firmographics` for size, revenue band and the technologies they
  run on.
- `company_funding` for how much capital is behind the roadmap — it tells you
  what they can copy and how fast.
- `company_jobs` on one or two of their listings for what is coming next. A
  cluster of hires on one function is a roadmap announcement nobody meant to
  make.
- `domain_keyword_overlap` on your domain and the strongest rival's, once you have identified one.

Strike any attribute an alternative also has. What survives is the only raw
material positioning can be built from.

## 3. VALUE — so what?

For each surviving attribute, answer "so what?" until you reach something the
buyer would put in a business case. In B2B that almost always terminates in
make money, save money, or reduce a risk that costs money. Three value themes
is plenty; five is a prospect who remembers none of them.

Then separate what your competitors have TESTED from what they have merely
PUBLISHED — the sharpest thing this data does:

- `ads_advertisers` on the competitor, then `ads_creatives`. Sort by run
  length using `first_shown` and `last_shown`. **Anything live 90+ days is a
  claim that survived their own performance review.** That is tested copy and
  it outranks anything on their website, which is untested.
- `ads_meta_advertisers` for the same read on social, where consumer and SMB
  spend goes — it returns run lengths as dates rather than as pixels, so the
  90-day test above is one you can apply directly.
- `domain_top_pages` on their domain shows which pages actually earn their
  traffic. The promise on those pages is the one the market rewarded.

A claim they run for a year and a claim they wrote once are different kinds of
fact. Label them differently in your report.

## 4. BEST-FIT CUSTOMERS — who cares a lot?

The segment for whom your differentiated value is not merely nice but decisive.
Find them in the evidence rather than in a persona document:

- `app_reviews` split by rating. Five-star reviews name what the delighted
  bought it for; three-star reviews name the one thing that blocks everyone
  else. Both are segment definitions written by customers.
- `keyword_overview` over your harvested terms, to see which segment's phrasing
  carries transactional intent and which is still browsing. Its intent column
  answers this without a second call.
- The competitor's job listings and firmographics tell you who they sell to
  now; the gap between that and who complains loudest is often your opening.

Name the characteristic that makes a customer a best fit — a trigger, a scale,
a constraint, a stack — not a demographic.

## 5. MARKET CATEGORY — what context makes your value obvious?

The category sets the buyer's expectations before you say anything. Pick the
one where your unique attributes read as table stakes for a leader rather than
as an odd extra. Then check that the market uses the word:

- `keyword_overview` on 5–15 candidate category nouns. A category with no
  search volume is a category you will have to fund the education for, and the
  same call's intent column tells you whether buyers already shop in that
  term or only read about it.
- `domain_serp_rivals` on the winning candidate: whoever owns that term today
  is who you are asking the buyer to compare you to.

Naming a category nobody searches for is a strategy. It is an expensive one,
and it should be chosen knowingly rather than by accident.

## 6. THE SILENCES

List what a serious product in this category should address and this
competitor never does — in their ads, their pricing page, their top pages,
their hiring. A silence sustained across every surface is either a deliberate
segment they have given up on or a weakness they cannot fix. Either one is
yours to take.

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

The filled positioning statement, one line per component. Then: their
converged bets (what they keep paying to say), their experiments (recent,
small, inconsistent), their silences, and the single sentence you would put at
the top of your own homepage as a result.

---

The same method is served as text at https://wutheringai.com/v1/free/skills/positioning-teardown, free and
without a token, and explained for a person at https://wutheringai.com/skills/positioning-teardown.
