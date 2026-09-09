---
name: pricing-power
description: >-
  Anchor price against what competitors actually charge and meter on, size willingness to
  pay from what the problem costs today, then run CAC, LTV and payback across three
  scenarios. Use when: Setting a first price, changing a price, or picking a value metric.
  Also when growth is fine and margin is not. Runs on Wuthering AI live data — about 12
  billed calls, $2.40. Ask for a token first if there is none.
---

# What do we charge, and does the money work?

**The job.** Tell me what to charge, what to charge for, and whether the unit economics survive a conservative case.

**The method.** Madhavan Ramanujam's willingness-to-pay discipline — price before you finish building, segment by need, and treat how you charge as more consequential than how much — followed by the CAC and LTV arithmetic done in the open.

**Deliver.** A price, a value metric, a packaging split into leaders, fillers and killers, and the LTV:CAC figure in three scenarios with the conservative one shown first.

## Before you start

`$ARGUMENTS` is the product being priced, in a sentence. If it is empty, ask for it in one question and stop until you have it.

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

**What this run costs.** About 12 billed calls, $2.40 at
20¢ per successful call. Stop at 20 ($4.00) — past
that you are confirming rather than learning. Failed calls are not charged. Say
the number out loud before a long run.

**Tools this method names.** `web_fetch`, `keyword_suggestions`, `keyword_overview`, `keyword_forecast`, `company_jobs`, `app_reviews`, `social_reddit_posts`, `ads_creatives`

**Other inputs, if the user supplied them.** `segment` — Buyer segment: b2c_sub, prosumer, b2b_smb, or b2b_mid. Sets funnel and churn defaults. `price` — Intended monthly price, if you have one. The run will try to break it. `competitor` — A competitor domain whose pricing page anchors the range.

---

## What is being priced

<the product being priced>

**FINDING URLS.** Several tools take a URL and cannot search for one
— `social_linkedin_posts`, `social_reddit_posts`, `social_reddit_comments`,
`company_jobs`, `company_person`, `web_fetch`. When you need a page, find its
URL with YOUR OWN web search first, using a site: filter. That costs nothing
and is exact. `web_search` does the same job for a billed call and is the
fallback when you have no search of your own. Never construct a URL from a company
name: a wrong URL comes back as a dead page, which reads as an absence of
evidence rather than as your mistake.

Ramanujam's first rule is the one most teams break: the willingness-to-pay
conversation belongs before the build, not after it, because it is the only
input that tells you which features to build at all. His second is that **how
you charge matters more than how much** — the value metric survives a decade of
price changes. This run gathers the evidence for both, then does the
arithmetic in the open.

## Gather first. Do not model on assumed numbers.

### 1. Anchors — what the market already charges

`web_fetch` 3–5 competitor pricing pages as `format=markdown`; switch to
`format=html` when the tiers sit in a table you need to read cell by cell.
For each, extract five things:

  FLOOR      the cheapest paid tier
  ANCHOR     the tier they visually push
  CEILING    the highest published price, and where "contact us" starts
  GATES      what you must buy the next tier to get
  METRIC     what they meter on — seats, usage, volume, outcomes

The metric is the finding. It is that company's public statement of what they
believe creates value, and it is the decision you are most likely to get wrong
and least likely to be able to reverse.

### 2. What the problem is worth today

- `company_jobs` on one or two listings for the role that does this work by
  hand, found by searching `site:linkedin.com/jobs/view "<the role>"`. A
  posted salary band is the cost of solving this problem with a person. Your
  price ceiling is a fraction of it, and the fraction is your argument.
- `keyword_overview` on the commercial terms: the CPC column is what a
  competitor pays for one click, which is the floor of what they believe a
  customer is worth.

### 3. Leaders, fillers and killers

Ramanujam's classification, sourced from what buyers volunteer rather than
what a survey prompts:

  LEADERS  the few capabilities people will pay more to get
  FILLERS  nice, but nobody moves tier for them
  KILLERS  present and people refuse to buy — often a pricing mechanic, not a
           feature: a seat minimum, an annual lock-in, an overage surprise

- `app_reviews` and `social_reddit_posts` on the competitor: search their
  threads for the word "worth it", for "we switched because", and for the
  complaints about billing rather than about features. Killers hide in billing
  complaints.
- `keyword_suggestions` on "<competitor> pricing", "<competitor> cost" and
  "<competitor> alternative". The alternative terms with real volume are a
  measure of how many people the current price has already pushed away.
- `keyword_overview` on that pool to separate people comparing prices from
  people researching the category.
- `ads_creatives` on the competitor: a price stated in a long-running ad is a
  price that converts.

## The arithmetic — show your work, never do it in your head

    CAC              = CPC / funnel_conversion
    LTV              = price × gross_margin / monthly_churn
    months_to_repay  = CAC / (price × gross_margin)
    reach_ceiling    ≈ monthly_search_volume × 0.04

Use `keyword_forecast` with a realistic bid to get clicks and cost at volume
rather than assuming the CPC scales.

SEGMENT DEFAULTS, if you have no measured funnel or churn. State which you used:

    b2c_sub    funnel 1.0%   churn 6.5%/mo
    prosumer   funnel 1.5%   churn 5.0%/mo
    b2b_smb    funnel 2.0%   churn 3.5%/mo
    b2b_mid    funnel 0.5%   churn 1.5%/mo

RUN THREE SCENARIOS. A base case on its own is marketing, not analysis.

    conservative   CPC ×1.25   funnel ×0.60   churn ×1.40
    base           as measured
    optimistic     CPC ×0.85   funnel ×1.40   churn ×0.70

**THE BAR: LTV:CAC at or above 3.0×, and the CONSERVATIVE case must clear it.**
If only the optimistic case clears, the answer is no. Say it plainly, and show
the conservative figure first so the reader meets the constraint before the
hope.

## Then decide the shape, not only the number

1. **The value metric.** Name it, and name what happens to the customer's bill
   when they succeed with your product. If the bill does not rise when their
   value rises, you have chosen a metric that caps you. If it rises faster than
   their value, you have chosen one that churns them.
2. **The packaging.** Put the leaders behind the tier you want people to buy.
   Fillers go in the base tier where they raise perceived value at no cost.
   Remove the killers or price around them.
3. **The segments.** Different needs, different packages — not one ladder of
   the same product in three sizes.

## Close with five options, each carrying the number it moves

  A. **Test it** at this spend, watching this metric, for this long
  B. **Charge more** — specifically this much, against this anchor
  C. **Change the metric** — to this one, which changes the bill like this
  D. **Narrow the buyer** — to this segment, which changes funnel to this
  E. **Walk away** — because this number does not move

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

The price, the metric, the packaging, and the LTV:CAC in all three scenarios
with the conservative one first. Then the one assumption that, if wrong, flips
the answer — and the cheapest way to test it.

---

The same method is served as text at https://wutheringai.com/v1/free/skills/pricing-power, free and
without a token, and explained for a person at https://wutheringai.com/skills/pricing-power.
