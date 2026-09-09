---
name: company-diligence
description: >-
  Read one company's trajectory from public evidence: branded demand year over year, the
  acquisition engine underneath it, whether that demand was earned or bought, and what
  payroll says ships next — then name the questions only a data room can close. Use when:
  Before an investment, a partnership, an offer, or a dependency you cannot cheaply
  reverse — any decision where the subject is someone else's company. Use
  positioning-teardown instead when the question is how to sell against them, and
  demand-validation when it is whether the market exists at all. Runs on Wuthering AI live
  data — about 13 billed calls, $2.60. Ask for a token first if there is none.
---

# Is this company actually growing?

**The job.** I am about to bet on this company — invest in it, partner with it, sign a contract with it, or take the offer. Tell me from the outside whether it is actually growing, which engine is carrying it, and what I would only learn after I signed.

**The method.** Bill Gurley's characteristics of a business worth a multiple, narrowed to the four an outsider can actually measure — growth, organic demand versus bought demand, concentration, and lock-in — and read as a series rather than a snapshot. The cheapest disqualifier runs first, so a run can end at call one with a real answer.

**Deliver.** A trajectory verdict with the series under it: branded demand year over year against the rival set, organic value and footprint over 24 months, which engine carries the growth and whether it was earned or bought, what payroll says ships next, and the three questions only a data room can answer.

## Before you start

`$ARGUMENTS` is the company you are diligencing: its name and its domain. If it is empty, ask for it in one question and stop until you have it.

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
20¢ per successful call. Stop at 22 ($4.40) — past
that you are confirming rather than learning. Failed calls are not charged. Say
the number out loud before a long run.

**Tools this method names.** `keyword_history`, `domain_overview`, `domain_traffic_history`, `domain_history`, `ads_creatives`, `ads_advertisers`, `domain_top_pages`, `web_search`, `company_jobs`, `company_profile`, `company_funding`, `company_firmographics`

**Other inputs, if the user supplied them.** `rivals` — Two or three rival domains, comma-separated. They ride in the same history call so a collection gap is separable from a real decline. `bet` — What you are about to commit, and what would make you walk away. `market` — Country to measure, if not the United States.

---

## The subject

<the company, and its domain>

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

Every other skill here is about your own product. This one is about someone
else's, which changes the rules: you cannot ask them anything, you cannot see
their numbers, and everything they publish is written to be read by you.

So work from instruments rather than claims, and remember that **a single
month is a number and only a series is a fact.** Two companies with the same
traffic this month are not in the same condition if one of them is halfway up
and the other halfway down.

Write the bet down before the first call: what you are committing, and the one
finding that would make you walk. A diligence run that discovers its own
threshold after the data arrives has not tested anything.

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

This run does not work straight down that ladder, and the reason is cost:
branded search is rung 3, but it is one call, it cannot be bought cheaply at
scale, and it disqualifies more subjects than anything below it. So the cheap
disqualifier goes first, and the money and salary rungs follow in steps 4 and
6, where they explain the trajectory rather than merely confirm it.

## 1. BRANDED DEMAND — the cheapest disqualifier, and it runs first

One `keyword_history` call, up to 700 terms for a single charge. Send the
subject's brand, two or three rivals' brands, and the intent-bearing compounds:
`<brand> pricing`, `<brand> alternatives`, `<brand> login`, `<brand> reviews`.

More people typing a company's name is the hardest-to-fake public signal that
it is growing. Nobody types a brand by accident, nobody buys the habit cheaply,
and it moves months before revenue does.

Read the **yearly averages**, not the last month. Then:

- **Rising year over year, and rising faster than the rivals in the same call**
  — the company is taking the category. Continue.
- **Flat while a rival rises** — they are losing share to a named party. That
  is the finding; the rest of the run explains it.
- **Flat, and the whole rival set is flat** — the category is not growing.
  Stop here and say so. This is a result, not a failed run, and it cost 20¢.

**KILL CRITERION, fixed now:** if branded demand for the subject is not higher
than it was twelve months ago, nothing later in this run rescues it. Traffic,
hiring and funding are all lagging or purchasable. This one is not.

**The trap.** A brand that is also an ordinary word cannot be measured this
way — the volume belongs to the word, not the company. When the brand is a
common noun, throw the bare term away and keep only the compounds above.
Reporting a common-word brand's search volume as company demand is the fastest
way to be confidently wrong in this run.

## 2. THE TRAJECTORY — and put the rivals in the same call

`domain_overview` on the subject first: one row, current position bands and
estimated traffic value, and the cheapest way to learn whether this domain has
enough footprint to be worth measuring over time at all.

Then `domain_traffic_history` with `targets=<subject>,<rival>,<rival>` and
`date_from` at least 24 months back.

**Batch the rivals in deliberately, even if you do not care about them.**
Public coverage has gaps, and a gap looks exactly like a collapse. A month
where every domain in the batch falls together and recovers the next month is
the instrument, not the market — and you can only see that because you asked
about more than one company. A solo history call cannot tell a bad month for
the company from a bad month for the index.

Two series come back per domain and they move independently:

  etv     estimated value of the organic traffic — the money
  count   how many keywords the domain ranks for — the footprint

Rising value on a shrinking footprint, and falling value on a growing one, are
both common and mean opposite things. Do not report one without the other.

## 3. RESOLVE THE CONTRADICTION WITH POSITION BANDS

`domain_history` on the subject. It returns the last few months only — it is
not the long series, step 2 is — but it splits the footprint by rank, which is
what settles step 2's ambiguity:

  pos_1, pos_2_3, pos_4_10     the positions that earn essentially all of it
  count                        everything, dominated by ranks 11-100

The tail is most of `count` and almost none of the money. So:

- **Top-10 bands holding or rising while `count` falls** — a content
  programme was cut, or the index pruned a tail nobody was reading. The
  business did not lose anything it was being paid for. Reporting this as a
  collapse is the most common error in an outside-in read.
- **Top-10 bands falling** — that is a real decline, whatever `count` does.
- Read the `paid` block in the same response. It is the measured paid
  footprint, and step 4 has to agree with it.

## 4. EARNED OR BOUGHT — Gurley's ninth characteristic

Demand a company created is worth a multiple. Demand it rents each month is
worth its margin. From outside you can tell them apart.

- **`ads_creatives` with `target=<domain>` is the first call, not the
  second.** It goes straight at the domain and returns the creatives with the
  dates each was first and last seen.
- `ads_advertisers` is for disambiguation only, and it matches loosely on the
  name: run it on a short brand and it will return verified advertisers whose
  names merely contain the string. **Check the `title` or `domain` on every
  row against your subject before you attribute one ad to them.** Borrowed
  spend is worse than no data, because it reads as evidence.

Then read the dates, because days live is the only performance signal public ad
data carries — an advertiser stops paying for a creative that does not work:

- **A small set of creatives, most of them running a year or more** — brand
  defence. Cheap, permanent, and not an acquisition engine. It should agree
  with a near-empty `paid` block in step 3.
- **A large set with a short median life, churning constantly** — bought
  growth. Real, and it stops the month the budget does. Discount the growth
  curve accordingly, and ask what the payback period is.
- **Sustained spend against a rival's brand terms** — someone is fighting for
  the same customer at renewal.

If step 3 says almost no paid keywords and step 4 shows long-lived creatives,
the two agree: the growth in step 2 was earned. Say that plainly — it is the
single most valuable sentence an outside-in read produces.

## 5. WHERE THE VALUE SITS — concentration

`domain_top_pages` on the subject. Two things to take from it:

- **The homepage's share of total organic value is the branded share.** A
  large share means the search channel is really a brand channel: the number
  will follow whatever creates the brand and will not survive it. A small
  share on a large total means an acquisition engine that works without the
  brand carrying it.
- **Which pages carry the rest.** A handful of pages holding most of the value
  is a concentration risk one ranking change can undo. The careers page
  appearing at all is hiring volume showing up in search.

## 6. WHAT PAYROLL SAYS SHIPS NEXT

Hiring is the roadmap a company has already paid for, visible months before
anything launches.

Find postings with your own search, or `web_search` on
`site:linkedin.com/jobs "<company>"`. Then `company_jobs` on one or two URLs,
which takes the posting's own URL.

Read the **shape of the list** before any single posting:

- A cluster of roles around one function is a bet being placed.
- Roles named for a second geography, or for an expansion motion, say the
  growth is meant to come from existing customers and new countries rather
  than new logos.
- Internal platform and sales-ops roles say the company is scaling process,
  which is what a company does after it has found something that works.
- `job_posted_time` on a live posting separates a company hiring today from a
  careers page nobody has pruned.

**Honest gap.** `base_salary` is empty far more often than not — bands are
published where the law requires them and rarely elsewhere. When it is absent,
the salary rung of the ladder degrades from "what they pay" to "which functions
they are buying", which is still a fact and still costs them money.

## 7. THE COMPANY RECORD — fire early, read last

`company_profile`, `company_funding` and `company_firmographics` resolve the
company upstream before they answer. They are the slowest calls here by an
order of magnitude and the most likely to time out. Start them at the beginning
of the run and read them at the end; retry a failure once, because failed calls
are refunded and a retry frequently succeeds. Let none of them gate the run:
the verdict has to stand on steps 1 to 6 whether or not these three answer.

What they are good for:

- `company_profile` — headcount and follower count. Headcount tracked against
  the last time anyone looked is the momentum signal; a single reading is only
  a size.
- `company_funding` — stage, number of rounds, investors, and whether they
  have been acquiring. A company making acquisitions is spending from strength.
- `company_firmographics` — revenue band, employees by function, and the
  technologies in use. The function split is the useful part: it says where the
  headcount actually went. It is also the least reliable of the three, so treat
  a run where it never answers as normal rather than as a blocked one.

**Honest gap.** The funding record reliably carries the *stage*, not the
*clock*. Round dates and amounts are frequently missing for private companies,
so months-of-runway is usually not computable from here. Do not infer it, and
do not let a stale round type stand in for one.

Where a total-visits figure comes back on the funding record, treat it as a
second, independent instrument — it counts all channels, not organic search —
and say so when you cite it. Two instruments agreeing is worth more than either
alone; two disagreeing is a finding you owe the reader.

## 8. THE VERDICT

Score only what you measured, on the four characteristics an outsider can see:

  GROWTH          branded demand YoY, and the 24-month value series
  EARNED/BOUGHT   creative longevity and the paid footprint
  CONCENTRATION   share of value in the homepage and the top pages
  LOCK-IN         evidence of expansion motion in hiring and product surface

Then name what you could not see. Growth accounting — new, resurrected and
expanded revenue against churned and contracted — is the thing you actually
want, and it needs numbers from inside the company. So finish by writing the
three questions the data room has to answer, each one aimed at a gap this run
identified rather than at a checklist. An outside-in run that ends with the
right questions has done its job even when it cannot close the answer.

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

The verdict on the four characteristics, each with the series behind it and the
call that produced it. The strongest evidence against your own conclusion. The
month you decided was a collection artefact and why. And the three questions
only a data room can close.

---

The same method is served as text at https://wutheringai.com/v1/free/skills/company-diligence, free and
without a token, and explained for a person at https://wutheringai.com/skills/company-diligence.
