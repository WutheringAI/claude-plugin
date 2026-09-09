---
name: crucial-test
description: >-
  Turn a belief the plan depends on into an explanation that cannot be bent to fit any
  result, name the rival explanations that would produce the same evidence, and pay only
  for the observations that would come out differently under each. Use when: When the
  question is not what the market looks like but whether the thing you already believe is
  true — a strategic assumption, a diagnosis of something that moved, or a disagreement
  between two people who both have data. Use demand-validation, positioning-teardown or
  company-diligence when the job is one of those; use this one when the belief cuts across
  them, or to try to kill a conclusion one of them produced. Runs on Wuthering AI live
  data — about 9 billed calls, $1.80. Ask for a token first if there is none.
---

# What would prove us wrong?

**The job.** The plan rests on one belief nobody has tested. Tell me the observation that would prove it wrong, then go and look — and tell me whether the refutation is already sitting in public data.

**The method.** Karl Popper's conjecture and refutation, sharpened by David Deutsch's test for a good explanation: it has to be hard to vary, so that no result can be accommodated by quietly moving a clause. Spend only where rival explanations predict different things — the crucial test — and judge a survivor by what else it predicts rather than by how well it fits.

**Deliver.** A verdict of refuted, survived or untestable — with the belief as it was written before the first call, the rival explanations it was tested against, the observation that discriminated between them and what it returned, the variation you were tempted to make and did not, and the one prediction a surviving explanation makes that you have not yet checked.

## Before you start

`$ARGUMENTS` is the claim the plan depends on, in one sentence. Write it as something about the world that could turn out to be false, not as a goal. If it is empty, ask for it in one question and stop until you have it.

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

**What this run costs.** About 9 billed calls, $1.80 at
20¢ per successful call. Stop at 16 ($3.20) — past
that you are confirming rather than learning. Failed calls are not charged. Say
the number out loud before a long run.

**Tools this method names.** `web_search`, `social_reddit_posts`, `keyword_history`, `keyword_overview`, `keyword_volume`, `keyword_intent`, `web_fetch`, `ads_creatives`, `company_jobs`, `domain_traffic_history`, `domain_history`, `domain_serp_rivals`, `keyword_suggestions`, `ads_advertisers`

**Other inputs, if the user supplied them.** `because` — Why you think it is true — the mechanism, not the evidence. This is the part the run tests. `subject` — What the belief is about: a domain, a brand, a product, or the terms buyers would search. Without one the run has nothing to point at. `decision` — What you would do differently if it turned out false. A belief no decision hangs on is not worth a call. `market` — Country to measure, if not the United States. Demand and ad coverage both vary sharply by country.

---

## The belief under test

<the belief the plan depends on, in one sentence>

Every other skill here starts from a question the instruments were shaped
for. This one starts from an answer you already hold and tries to kill it. The
procedure does not change with the subject — the same gates work on a demand
claim, on a rival's strategy, on a traffic drop, and on a disagreement between
two people who both have data. What changes is where you aim, not how you
decide.

It is also the cheapest run on this list, and that is the argument rather than
a concession. Most of the work is free, and the paid part is short because
most calls you could make cannot change the answer.

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

## Steps 1 to 4 cost nothing. Many runs should end inside them.

The expensive part of research is the calls. The cheapest way to make a call
worth its price is to know, before it returns, which result would change your
mind.

### 1. Write the belief as an explanation, not a prediction

"Demand is growing" is a prediction. "Demand is growing because the rules
changed in March, so buyers who used to handle this in a spreadsheet now have
to file it" is an explanation. Only the second tells you where to point an
instrument, because only the second says what else would have to be true.

Write the mechanism. If you cannot write one, you do not yet have something to
test — you have a number you expect to see, and any number can be explained
after it arrives.

### 2. Try to save it, in writing. This gate kills the most runs.

Suppose the data comes back against you. Which clause of your explanation would
you adjust to keep the belief alive? Write that clause down now.

An explanation you can rescue from any result explains nothing, because it
forbids nothing. If you found such a clause you have two choices and only two:
fix it — commit in writing to the version you will not move — or record that
the belief is not yet testable and stop.

Do this before the calls. Afterwards it is indistinguishable from reasoning.

### 3. Name the observation that would refute it, and check that it exists

State one result, from one named tool, at one number, that you would accept as
a refutation. Not evidence you would weigh. A refutation.

  TOOL       the call you would make
  ARGUMENT   what you would send it
  RESULT     the shape of answer that kills the belief
  THRESHOLD  the number, fixed now

If no public observation could bear on the belief either way, it does not touch
anything this API can reach. No amount of spending fixes that. Say so and stop.

**KILL CRITERION 1, at zero calls.** No tool, no argument, no threshold — no
run. Report it as the finding. A belief that survives because it was never
exposed is the most expensive thing on this list, and it costs nothing to
catch.

### 4. Write the rivals. At least two, and make one of them boring.

You cannot read an explanation off a dataset. Every number is consistent with
several stories, and the one you notice is the one you walked in with. So bring
the others deliberately.

Write at least two rival explanations for the same evidence. The boring one is
usually right and is almost never the one a team arrives with. Four account for
most of it:

  THE INDEX MOVED         coverage or measurement changed, not the subject
  THE CATEGORY MOVED      everyone rose or fell together; you did nothing
  THE INSTRUMENT IS BLIND thin coverage here, not an empty market
  NOTHING MOVED           you are reading a level and calling it a trend

A run with one candidate can only confirm. Confirmation costs the same 20¢ as
refutation and is worth less.

Where do rivals come from when you have none? From people describing the same
thing differently. Find the thread with your own search, or `web_search`, then
`social_reddit_posts` on the post itself — it takes the post's own URL and
refuses a subreddit front page. Read it for candidate mechanisms, not for a
verdict. Anecdote sits at the bottom of the ladder and its job here is to
generate explanations, never to choose between them.

## Steps 5 to 9 are the run itself. This is where the money goes.

### 5. Derive the crucial test — and pay for nothing else

For each pair of belief and rival, write what each predicts for a specific
call. Then spend only where the two predictions differ.

An observation both explanations predict cannot separate them. It will come
back, it will feel like progress, and it will move nothing. That is the whole
budget rule here.

**A belief about demand** — "people want this", "this is growing".

Not `keyword_volume` on its own: a large number is predicted by real demand,
by a fad, and by having picked terms broader than your product. Instead one
`keyword_history` call — up to 700 terms for a single charge — carrying your
terms AND a control set from an adjacent category you believe is unaffected.
Your terms rise while the controls do not: the subject moved. Both rise: the
season or the index moved. Then `keyword_intent` on the same list, which
separates people who want to buy from people who are curious. The two have the
same volume and different worth.

**A belief about a rival** — "they are betting on this", "their strategy is
that".

Not their website. Everything a company publishes is written to be read by you,
so `web_fetch` on a page returns what they claim, which no rival explanation
disputes. Instead `ads_creatives` with `target=<their domain>`, and read
`first_shown` and `last_shown` on every row. A creative running 90+ days
survived their own performance review; nobody sustains a losing ad for a
quarter. Then `company_jobs` on one or two live listings, found with your own
search. A message they pay to keep running and a role they pay a salary for are
both claims that cost money to make. A homepage is free.

**A belief about a move** — "we lost ground", "the market shifted", "they took
our traffic".

Not a solo call on your own domain. Instead `domain_traffic_history` with
`targets=<you>,<rival>,<rival>` and `date_from` at least 24 months back. This
is the crucial test in its cleanest form: one argument different, and the two
explanations predict different shapes. A month where every domain in the batch
falls together and recovers the next is the instrument, not the market — and
you can only see that because you asked about more than one. Then
`domain_history` on the subject, and read the position bands rather than
`count`.

**A belief about your position** — "we are the obvious choice", "they would
pick us".

Not your own list of competitors. Instead `domain_serp_rivals` on the terms a
prospect would actually type: it takes the keywords, not your domain, and
returns who shows up when the buyer asks. Then `keyword_suggestions` on
"<brand> alternative", for yours and for theirs, which measures the population
each current answer has already pushed away.

### 6. Run it. Four observations that look decisive and are not.

Each of these has already produced a confident wrong answer in a real run of
another skill here.

**A falling `count` is not a decline.** One subject's ranked-keyword count fell
60% over six months while it held more top-ten positions at the end than at the
start. A pruned tail and a collapse both predict a falling `count`, so `count`
cannot separate them. `domain_history`'s position bands — `pos_1`, `pos_2_3`,
`pos_4_10` — can. The tail is most of `count` and almost none of the money.

**A name match is not an advertiser.** `ads_advertisers` matches loosely on the
name: run on a short brand it returned four verified advertisers, none of them
the subject, while the subject's own forty creatives came back from
`ads_creatives` with `target=<domain>`. Go to the creatives first and use
`ads_advertisers` only to disambiguate, checking `title` or `domain` on every
row before you attribute one ad to anyone. Borrowed evidence is worse than no
evidence, because it reads as evidence.

**An empty result is not an empty market.** Run the same call, unchanged, on a
control you are certain about — a term you know has volume, a domain you know
ranks. If the control comes back empty too, the instrument is blind for this
query or this country and the belief is untested, not refuted. One extra call
buys the difference between "there is nothing there" and "I cannot see". Make
it before you report an absence.

**A withheld row is not a zero.** BATCHING above says it, and it belongs here
too, because it is the same error wearing different clothes. A trimmed response
reports how many rows it held against how many it returned. The terms you did
not get were withheld, not measured at zero.

### 7. If it was refuted, the run finished. It did not fail.

Write down the variation you were tempted to make.

You will feel it — the clause from step 2, offering itself again now that you
know which way the data went. Record it in the words you would have used. That
record is the most valuable thing this run produces, because in three months
somebody will propose exactly that variation, and by then there will be no
memory that it was invented to save a belief the evidence had already killed.

Then stop. A refutation reached in four calls is the best outcome available
here, and it is what the free gates were for.

### 8. If it survived, make it pay: name what else it predicts

A conclusion that accounts for exactly the data you bought is not an
explanation, it is a summary of your receipts. An explanation worth keeping
reaches further than the problem it was built for — it makes claims about
things you were not looking for, and those claims can be checked.

So state one consequence of the surviving explanation that you have NOT checked
and that the rivals do not share. Then either buy it in one call or write it as
the first call of the next run.

**KILL CRITERION 2.** If the surviving explanation predicts nothing beyond the
observations you already paid for, you did not learn a mechanism. You learned
that some numbers moved together. Say that in those words, so it cannot be
quoted later as the reason for anything.

### 9. Survived is not true. Write the expiry.

It survived this test, at this threshold, in this country, on this date, with
these instruments. All five are load-bearing and all five decay. Expect your
best current explanation to contain something false; that is the normal
condition, not a failure of this run.

So finish by writing what would have to change for the run to be worth
repeating — a rival launching, a season turning, the threshold crossed from the
other side. A belief with no scheduled re-test becomes an assumption again
inside a quarter, and the next run will start from it instead of testing it.

## Where the instruments are blind

- **Mechanism is what you are testing and what public data is worst at.** You
  can measure that something moved, and with controls whether it moved for the
  subject or for everyone. WHY it moved is inference. So the strongest verdict
  usually available here is "this rival is now excluded", not "the belief is
  confirmed" — and the first is worth more anyway.
- **Intent is not localized.** Intent is classified per language and not per
  country — that is true of the `keyword_intent` column wherever it is read,
  `keyword_overview` included — so for a belief about one market the intent
  split is measured across places rather than in one. Volume and history DO
  take a location; localize with those and read intent as a shape, not a level.
- **Coverage thins outside the largest markets.** An absence found far from the
  United States is much more likely to be the instrument than one found inside
  it, which is why the control call matters more the further out you go.
- **Nothing here sees your own numbers.** A belief about what YOUR change caused
  cannot be tested from outside. What can be tested is whether the world around
  it moved at the same time, and whether it moved for your competitors too.

## The verdict

One of four, and only these four:

  REFUTED       the discriminating observation came back against the belief.
                Give the call, the number, and the threshold fixed in step 3.
  SURVIVED      it came back for the belief, and at least one rival is now
                excluded by name. Give the rival, and what excluded it.
  INCONCLUSIVE  the call was made and did not separate them after all. Name
                the one further call that would, as the rules below require.
  UNTESTABLE    nothing available here could have separated them, and gate 3
                should have caught it. Say what a different instrument would
                need to see.

The last two are different failures and the difference matters: INCONCLUSIVE is
an instrument that came up short, UNTESTABLE is a question that was never
exposed to one. "Supported" is not a verdict. Neither is "directionally
correct". A run that cannot say which of the four it reached has not finished.

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

The belief as you wrote it before the first call, and the clause you committed
not to move. The rivals. The observation you chose, and why it discriminates
rather than merely relates. What it returned. The verdict, one of the three.
The variation you were tempted to make. And, if it survived, the one prediction
it makes that you have not yet paid to check.

---

The same method is served as text at https://wutheringai.com/v1/free/skills/crucial-test, free and
without a token, and explained for a person at https://wutheringai.com/skills/crucial-test.
