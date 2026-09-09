---
name: channel-bet
description: >-
  Score every plausible channel against the product's own characteristics, measure the
  reachable demand and the cost of entry for each, and commit to one with its CAC and its
  ceiling stated. Use when: After the product works and before the growth hire. Also when
  a channel that used to work has stopped and you need the next one chosen with evidence
  rather than by rotation. Runs on Wuthering AI live data — about 13 billed calls, $2.60.
  Ask for a token first if there is none.
---

# Where do the next 1,000 customers come from?

**The job.** Pick one acquisition channel we can afford, prove it works for a product like ours, and tell me its ceiling before we commit a year to it.

**The method.** Brian Balfour's product-channel fit — products are built to fit channels, channels do not mold to products, and distribution follows a power law — with Ethan Smith's topic clustering used to size the search channel honestly.

**Deliver.** One named channel with its CAC, its reachable ceiling, the product change it requires, and the measured evidence that it works for a product with these characteristics.

## Before you start

`$ARGUMENTS` is the product, and a domain if it has one. If it is empty, ask for it in one question and stop until you have it.

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

**Tools this method names.** `keyword_ideas`, `keyword_overview`, `keyword_volume`, `keyword_intent`, `keyword_difficulty`, `keyword_forecast`, `domain_serp_rivals`, `domain_top_pages`, `domain_traffic`, `domain_overview`, `ads_advertisers`, `ads_creatives`, `app_search`, `app_keywords`, `app_top_charts`, `social_youtube_search`, `social_reddit_posts`, `company_jobs`

**Other inputs, if the user supplied them.** `price` — Price or ACV. This is what decides which channels can pay for themselves. `competitor` — A competitor domain whose working channels are worth reading. `market` — Country to measure, if not the United States.

---

## The product

<the product, and its domain if it has one>

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

Balfour's rule governs this whole run: **products are built to fit channels;
channels do not mold to products.** So the first question is never "which
channel should we try" but "which channels can a product with these
characteristics survive in". And distribution follows a power law — the
companies that get to real scale take 70%+ of their growth from one channel.
A run that ends with four channels ranked equally has not made the decision it
was run to make.

## 1. Write the product's characteristics down first

Four attributes decide channel fit, and all four are known before any call:

  PRICE / ACV         what one customer is worth in year one
  TIME TO VALUE       hours from signup to the promised outcome
  VALUE BREADTH       how much of the addressable population it applies to
  FREQUENCY           how often the job recurs

Then apply the constraints, which are arithmetic rather than opinion:

- **Paid** needs quick time to value and a transactional model that returns
  the cash before the ad bill. Sub-$100 ACV with a 30-day sales cycle cannot
  fund clicks.
- **Search** needs a problem people put into words before they buy. A problem
  with no query has no search channel, whatever its size.
- **Virality** needs the product to be better with more users, and a short
  cycle. Bolted-on referral schemes are not this.
- **Sales** needs an ACV that pays a salary, and a buyer with a budget line.
- **App store** needs the buying decision to happen inside a store.

Rule out the impossible ones now, in writing, with the number that rules them
out. That is half the answer and it costs nothing.

## 2. Measure each surviving channel with its own instrument

### Search

- `keyword_ideas` on the problem, then `keyword_overview` on everything it
  returns — volume, intent and difficulty in one call.
- **Cluster into topics, not keywords.** Ethan Smith's test: two terms belong
  on one page when the same domains rank for both, and on separate pages when
  they do not. Run `domain_serp_rivals` on each candidate head term and
  compare the domain lists. Sizing a "keyword" that is really six topics
  overstates the channel; splitting one topic into six pages loses to whoever
  did not.
- The difficulty column on the head term of each cluster is the cost of entry.
  `keyword_difficulty` scores head terms separately when the cluster ran past
  what one `keyword_overview` call carried.
- `domain_top_pages` on whoever owns the cluster today shows the page TYPE
  that wins it — a listicle, a comparison, a tool, a template. That is what you
  would have to build, not merely what you would have to write.
- `domain_traffic` or `domain_overview` on those winners sizes the prize.

### Paid

- `keyword_forecast` at a realistic bid gives clicks and cost at volume;
  divide by your funnel rate for a CAC that is measured rather than assumed.
- `ads_advertisers` on the money terms, then `ads_creatives`. An advertiser
  running the same creative 90+ days is proof the channel pays for someone with
  a business model like theirs — check that it IS like yours before borrowing
  the conclusion.

### App store

- `app_search` on the buyer's phrase, `app_keywords` on the incumbent, and
  `app_top_charts` for the category's traffic shape.

### Video, community and social

- `social_youtube_search` on the buyer's question. View counts on a
  how-to video are unmet demand with a timestamp, and the channel that made it
  is a distribution partner you could pay.
- `social_reddit_posts` on the communities where the problem is discussed,
  for whether recommendations actually happen there or whether it is a
  complaint board.

### Sales and outbound

- `company_jobs` on competitors' listings. A competitor hiring SDRs and AEs
  has concluded their buyer needs a human; a competitor hiring content and
  lifecycle has concluded the opposite. Their conclusion is evidence, not
  proof — but it is evidence that cost them a salary.

## 3. Score the survivors on one table

  Channel | Reachable/mo | CAC | Payback | Time to first result | Ceiling | Product change required

**Ceiling** is the one column teams skip and the one that decides the year: a
channel that can only ever deliver 300 customers a month is not a growth
strategy for a company that needs 3,000, however good its CAC.

## 4. Commit to one

Name it. State its CAC, its ceiling, and the product change it demands — there
is almost always one, because the product is what moves. Name the second
channel only as the hedge, and say the specific number that would make you
switch to it. Then name the cheapest experiment that would prove or kill the
first inside 30 days.

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

The one channel, its numbers, the product change, the 30-day test, and the
list of channels you ruled out with the figure that ruled each one out.

---

The same method is served as text at https://wutheringai.com/v1/free/skills/channel-bet, free and
without a token, and explained for a person at https://wutheringai.com/skills/channel-bet.
