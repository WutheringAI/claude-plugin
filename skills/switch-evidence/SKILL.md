---
name: switch-evidence
description: >-
  Gather the language of people switching into and out of this category, code every quote
  to the force that drives it, size each theme against real search demand, and return a
  50/50 roadmap. Use when: Quarterly planning, a churn spike, or any roadmap argument that
  has become a contest of opinions. Also before a competitor's renewal season, when
  switching language peaks. Runs on Wuthering AI live data — about 11 billed calls, $2.20.
  Ask for a token first if there is none.
---

# What should we build next?

**The job.** Tell me what to build next from what users actually say when they switch, not from what they say in a survey or what we wish they said.

**The method.** Bob Moesta's four forces of progress and the switch interview, run against public text at a scale interviews cannot reach; Rahul Vohra's 50/50 split for turning the result into a roadmap.

**Deliver.** Themes ranked by size, each carrying its force, three verbatim quotes, a measured demand figure, and the specific change that would move it — split 50/50 between deepening what works and removing what blocks.

## Before you start

`$ARGUMENTS` is your product or the category you are planning inside. If it is empty, ask for it in one question and stop until you have it.

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

**What this run costs.** About 11 billed calls, $2.20 at
20¢ per successful call. Stop at 20 ($4.00) — past
that you are confirming rather than learning. Failed calls are not charged. Say
the number out loud before a long run.

**Tools this method names.** `keyword_suggestions`, `keyword_overview`, `web_search`, `app_reviews`, `app_details`, `social_reddit_posts`, `social_reddit_comments`, `social_youtube_search`, `social_youtube_comments`, `social_linkedin_posts`, `web_fetch`

**Other inputs, if the user supplied them.** `competitor` — The competitor people switch to or from. Switching language clusters around a name. `app_id` — App Store or Google Play id, if a competitor ships a mobile app. Reviews are the richest source here. `market` — Country to measure, if not the United States.

---

## What we are planning

<your product, or the category you are planning inside>

**FINDING URLS.** Several tools take a URL and cannot search for one
— `social_linkedin_posts`, `social_reddit_posts`, `social_reddit_comments`,
`company_jobs`, `company_person`, `web_fetch`. When you need a page, find its
URL with YOUR OWN web search first, using a site: filter. That costs nothing
and is exact. `web_search` does the same job for a billed call and is the
fallback when you have no search of your own. Never construct a URL from a company
name: a wrong URL comes back as a dead page, which reads as an absence of
evidence rather than as your mistake.

Bob Moesta's frame, and the whole reason this run exists: people do not buy
products, they switch. A switch happens when

    PUSH (frustration with today) + PULL (attraction to the new)
      >  ANXIETY (fear of the switch) + HABIT (what they must give up)

Feature requests are pull. Pull is the force teams over-serve, because it is
the only one that looks like a roadmap. Most stalled products are losing to
anxiety and habit, and the fixes for those are migration tools, proof,
defaults, and guarantees — work that never wins a prioritisation meeting
because it does not look like a feature.

The switching moment is where the job reveals itself, so go where switching is
discussed rather than where your product is discussed.

## 1. Find the switching moments

- `keyword_suggestions` on "<competitor> alternative", "switch from
  <competitor>", "<competitor> vs". Then `keyword_overview` on everything it
  returns, which prices and classifies them in one call. **This is your first measurement,
  not just a search step:** volume on "<competitor> alternative" is the size of
  the population already in motion, and it is the cheapest number in this
  whole run.
- Find the threads with your own web search — `site:reddit.com "<competitor>"
  alternative`, `site:reddit.com "switched from <competitor>"` — or
  `web_search` if you have none.
- `social_youtube_search` on "<competitor> vs" and "<competitor> review".
  Comparison videos are switch interviews someone else already filmed.

## 2. Read the words, in the buyer's own phrasing

- `app_reviews` on the competitor, run twice: `sort_by=most_recent` for what
  is true now, and filtered to low ratings for the push. Five-star reviews name
  the pull. Three-star reviews are the most valuable rows in this entire run —
  someone who almost stayed, naming the one thing that stopped them.
- `social_reddit_posts` on the threads you found, then
  `social_reddit_comments` on the two or three where the discussion is real
  rather than a link drop.
- `social_youtube_comments` on the comparison videos. People announce their
  switch in comments in a way they never do in reviews.
- `social_linkedin_posts` on a post where a practitioner explains a migration,
  for the B2B version of the same evidence.
- `app_details` or `web_fetch` on the competitor's changelog or release
  notes: what they shipped last quarter tells you which complaints they have
  already answered, so you do not build a fix for a problem that no longer
  exists.

Quote verbatim, always. The buyer's exact words are the deliverable — a
paraphrase loses both the emotion and the search term.

## 3. Code every quote to one force

Take each quote and mark it PUSH, PULL, ANXIETY or HABIT. Do it per quote, not
per person; one review routinely carries three forces.

  PUSH      "I was spending every Friday afternoon reconciling this by hand"
  PULL      "the thing that sold me was seeing it work on my own data"
  ANXIETY   "I have four years of history in there and I could not risk it"
  HABIT     "my whole team already lives in the other tool"

Then count. **The distribution is the finding.** A category where anxiety
dominates is won with migration, proof and guarantees, not with features — and
a roadmap of features aimed at an anxiety-dominated market is how a good
product loses to a worse one.

## 4. Size each theme before you rank it

A theme quoted by nine people may be smaller than a theme quoted by two.

- `keyword_overview` on the phrases people used for each theme — their words,
  not your feature name. One call carries both halves of the reading: a theme
  people search commercially is one they would pay to fix, and a theme searched
  informationally may be a content answer rather than a product one.

Themes with no measurable search volume are not automatically small — some
problems have no query — but say so explicitly and name what you are relying
on instead.

## 5. Build the 50/50 roadmap

Rahul Vohra's split, which exists to stop a roadmap becoming pure defence:

- **Half: deepen what the delighted already love.** From the five-star and
  strongest pull evidence. This is what makes people stay and tell others, and
  it is the half that gets cut first under pressure.
- **Half: remove what blocks the nearly-persuaded.** From the three-star and
  the anxiety/habit evidence. Each item names the force it removes, not the
  feature it adds.

Every line carries: the force, the size, three verbatim quotes, and the
specific change. A line with no quote is an opinion that got into the document.

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

The force distribution as counts. The ranked themes with quotes and sizes. The
50/50 roadmap. And the one theme you expected to see and did not — an absence
is a finding when you went looking for it on purpose.

---

The same method is served as text at https://wutheringai.com/v1/free/skills/switch-evidence, free and
without a token, and explained for a person at https://wutheringai.com/skills/switch-evidence.
