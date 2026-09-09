---
name: idea-maze
description: >-
  Map the category around one domain as an idea maze — the forks it has already run, who
  took each branch, which walls are still walls and which have moved — then return the one
  open position with the offer that takes it: buyer, bundle, price metric and message,
  decided together. Use when: When you have a category and a domain but not a position:
  choosing where to enter, what to build next to, or where to expand. Use
  positioning-teardown instead once the product exists and the job is to sell it better,
  and demand-validation when the question is whether any market is there at all. This one
  runs before both of them and hands them their subject. Runs on Wuthering AI live data —
  about 18 billed calls, $3.60. Ask for a token first if there is none.
---

# Where is the unoccupied position in this category?

**The job.** We know the category and we know the incumbents. Map the forks this category has already run, show me who took which branch and which branch killed them, and tell me which one is still open — with the price, the bundle and the message that go with it.

**The method.** Balaji Srinivasan's idea maze, popularised by Chris Dixon's essay of the same name: a good idea is not a sentence but a detailed path through a maze whose turns lead to treasure or to certain death, and whose walls move as technology changes. W. Chan Kim and Renée Mauborgne's eliminate-reduce-raise-create grid forces the subtraction that makes a chosen position defensible; the bundle follows Madhavan Ramanujam's leaders, fillers and killers.

**Deliver.** The maze as a tree: the forks this category has already run, who took each branch, which branches are dead and which walls have since moved — plus the one open position, scored on demand, intent and occupancy, and the offer that takes it: buyer, bundle, price metric and message, with what it deliberately gives up and how long it stays yours.

## Before you start

`$ARGUMENTS` is the domain that anchors the maze — yours, or the incumbent whose category you want to enter. Use the domain they serve today, not a retired one. If it is empty, ask for it in one question and stop until you have it.

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

**What this run costs.** About 18 billed calls, $3.60 at
20¢ per successful call. Stop at 31 ($6.20) — past
that you are confirming rather than learning. Failed calls are not charged. Say
the number out loud before a long run.

**Tools this method names.** `domain_categories`, `domain_relevance`, `domain_rankings`, `domain_competitors`, `domain_serp_rivals`, `domain_traffic_history`, `web_fetch`, `keyword_history`, `keyword_ideas`, `keyword_related`, `keyword_overview`, `keyword_volume`, `keyword_intent`, `keyword_difficulty`, `domain_top_pages`, `ads_creatives`, `ads_meta_advertisers`, `ads_meta_library`, `company_jobs`, `app_reviews`, `social_reddit_posts`

**Other inputs, if the user supplied them.** `angle` — The path you already favour, in one sentence. The run will try to kill it first. `buyer` — The segment you intend to serve, if you have a view. A role and a scale is enough. `price` — The price point you would enter at. Whitespace at $20 a month and at $2,000 a month are different rooms. `market` — Country to measure, if not the United States.

---

## The anchor

<the domain that anchors the category>

## What you are building

Balaji Srinivasan's frame, which Chris Dixon's essay carried further: an idea
is not a point, it is a maze. "I have an idea for doing music and movies on
the internet" is one sentence. The maze is the tree of forks underneath it —
open source or closed, free or paid, per download or subscription, music only
or music and movies — and each leaf is a company. Some leaves hold treasure.
Napster and Kazaa took the wrong branch and are dead.

Srinivasan's test is blunt: **if your idea is one sentence, you do not have a
good idea.** What you should be able to produce instead is a detailed path
that is aware of every competitor and every branch already taken.

Dixon adds what a founder worth backing actually holds: a sense for the
history of the industry, the players in the maze, the casualties of the past,
and **the technologies likely to move walls and change assumptions.** That
last clause is why this run has a step for it. The maze is time-varying.
Pandora was a struggling idea until the iPhone put a computer in every pocket,
and then it was a different company. Doors open. Doors also close, because an
incumbent can cross a bridge a startup cannot.

This run draws that map from outside, from one domain. It cannot ask anyone
anything. What it can do is read where the demand is, where the money is,
which branches are taken, which branches killed whoever took them, and which
walls have moved since.

## Fix these before the first call

  PATH YOU BELIEVE IN   your favoured branch, as a path and not a sentence
  WALL YOU EXPECT       what you think stopped whoever tried it before
  PRICE FLOOR           the number below which this is not a business for you
  WALK-AWAY             the finding that would end the run

An empty room is empty for a reason until you have found the reason. Most
whitespace is desert: nobody is standing there because nobody could ever pay
to stand there. Steps 6 and 7 exist to tell the two apart, and a run that
skips them returns a beautiful map of a place with no water.

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

## 1. THE BOUNDARY — what business is this domain actually in?

Three calls on the anchor, answering three different questions.

- `domain_categories` on the anchor. It returns numeric category codes with
  organic metrics and **no labels**, so treat it as orientation and nothing
  more: it tells you how many distinct categories the domain has presence in
  and how lopsided that presence is. Do not build the map on it.
- `domain_relevance` with `target_type=site`. What the index considers this
  site to be ABOUT, with volume and CPC per term.
- `domain_rankings` with `limit=1000`. What it actually WINS. **Pull it deep
  on the first call.** At a limit of 150 you will find hundreds of terms
  "missing" from the ranked set that are merely below the cut, and report a
  gap that is really a truncation.

Then compute three numbers, and all three are findings.

**The footprint, and whether the instruments can see at all.** Count the
ranked terms. Under about fifty — a stated default, not a measured constant —
the domain tools are blind on this anchor and every ratio below is noise: an anchor that ranks for one keyword is not a
small player in its category, it is absent from the index. That is a finding
about the company, not a failed run — but it means **the maze has to be
anchored on an incumbent instead.** Keep your subject as the subject; move the
anchor to the domain that holds the category's money terms, and read every
later step as being about the room rather than about them.

**The branded share.** Count the ranked terms containing the brand name. A
domain whose ranked set is mostly branded has a brand footprint, not a
category footprint — it wins its own name and does not hold the ground its
category is fought on. That single ratio changes how you read step 2.

**Relevance minus rankings.** Terms the index associates with this domain that
it does not rank for. **Deduplicate first:** `domain_relevance` returns
variant phrasings that share one volume figure and one CPC — "task management
software", "task and project management software", "task mgmt software" all
carrying the same number. Collapse rows on (volume, CPC) or you will size the
category at two or three times its real width. What survives, ranked by volume
times CPC, is ground this domain is credited with and does not hold. If the
anchor is yours, that is the cheapest expansion anyone will hand you. If it is
a rival's, it is the part of their category they have claimed and not
defended.

## 2. THE ROSTER — and read the branded share before you trust it

- `domain_competitors` on the anchor: rivals by keyword-set overlap.
- `domain_serp_rivals` on the 10–20 highest-value terms from step 1: who owns
  the battlegrounds. It starts from keywords rather than from a domain, so it
  returns whoever holds those terms whether or not they overlap the anchor.

**The trap, and it is severe.** `domain_competitors` measures overlap across
the anchor's WHOLE keyword set. When that set is mostly branded, the domains
that overlap it are wherever the brand is discussed — video platforms, forums,
publishers, the anchor's own template ecosystem — and not one of them is a
competitor. Above roughly half branded, treat `domain_competitors` as a map
of the brand's audience and build the roster from `domain_serp_rivals`
instead. The two lists routinely share almost nothing, and the disagreement
tells you which one you are holding.

**Below the footprint floor it degrades further.** With a handful of ranked
terms, `domain_competitors` returns whoever shares your one accidental
keyword — a page of unrelated businesses that happen to rank for a phrase in
your privacy notice. It is not wrong; it is answering the question you asked
with the only data you gave it. Do not read a roster out of it.

**Keep the publishers.** On a category's money terms the largest holders of
estimated value are usually not products at all but review sites, forums and
listicles. They are rooms, and they are the rooms collecting the rent.

## 3. THE DEAD ENDS — the casualties, read against their cohort

`domain_traffic_history` with `targets=` the entire roster and `date_from`
at least 36 months back. One billed call takes up to 1,000 domains: send every
domain you have, plus the ones you suspect are already dead. The marginal
domain is free and the corpses are the point.

**Never read a curve on its own.** Build a roster index first: normalise each
domain's series to its own first month, then take the median across the roster
per month. Whole categories move together, and a category's measured organic
value can fall by a third over three years while every company in it is
trading normally. Judge each domain against that index, never against zero:

  OUTRUNNING     rising against the index — an occupied branch someone is winning
  WITH COHORT    moving as the category moves; the branch is neither hot nor dead
  LAGGING        losing ground steadily; a branch going wrong, not yet gone
  DEAD END       collapsed while the cohort held — somebody hit a wall here
  NO DATA        a flat zero series. The product is gone, not declining

An absolute rule marks the whole category dead. A relative one finds the four
or five domains that actually failed, and those are your walls.

**A ratio off a base near zero is not a growth rate, in either direction.**
A domain that went from an estimated value of 1 to 25,000 and one that went
from 1 to 0 will both produce spectacular multiples and neither is evidence.
Read the absolute level alongside the ratio and discard any domain whose
starting value was too small to move. Your own anchor is often one of them.

**Then cluster the dead ends by what they SOLD, not by domain.** One company
failing is a company failing. The finding is several independent companies
failing on the same branch — the same promise, the same buyer, the same price
shape — because that is a wall rather than a management team. A branch where
five or six unrelated domains all fell against a holding cohort is the
strongest negative result this run produces, and it is invisible if you read
the list one company at a time.

**Four checks before you call any fall a wall.**

- **A sibling rising in the same batch.** A company that moved domains shows
  as a collapse and a rocket side by side. Batching is what makes this free to
  see, and it is why the roster goes in whole. Check the anchor itself: if the
  anchor is the retired half of a migration, restart the run on the live one.
- **`web_fetch` the two most interesting collapses** as `format=markdown`.
  It answers with the page as one markdown string rather than a row set. A
  dead site, a redirect to a new brand and a trading company with a pivoted
  homepage are three different findings and only one is a wall. **When the
  collapsed company is still trading, what it sells NOW is the shape of the
  wall** — a consumer app whose survivors all sell to teams tells you the wall
  was the buyer and the price, not the product. Where the survivors escaped to
  is the most useful sentence on the branch.
- **Confirm an OUTRUNNING domain before you treat its rise as category
  evidence.** `domain_top_pages` on it, and read what those pages are about.
  A domain can triple on generic content that has nothing to do with this
  category — interview questions, salary guides, job descriptions — and
  counting it as demand for the category is the same error as attributing
  another company's ad spend.
- **Name collisions.** Two unrelated companies with similar domains land in
  the same batch and read as one story. Check what each domain actually sells.

## 4. THE DOORS — which walls have moved

This is the step that separates a map from a history lesson, and it is
Srinivasan's point about a time-varying maze made measurable.

`keyword_history` on up to 700 terms in one call. Send three sets together:
the category's established vocabulary, the vocabulary of any enabling shift
you suspect, and the exact phrases the dead ends from step 3 were built on.

**Read the monthly series, not a yearly average.** The response nests each
point's volume inside `keyword_info.monthly_searches` rather than putting it
on the row, and a reader that misses the nesting concludes there is no history
at all. A single month an order of magnitude above its neighbours is an
artefact until a second instrument agrees.

Three shapes, and each means something different:

- **A door that opened.** A phrase at nothing three years ago and at thousands
  a month now dates the shift to the year. That is a wall that moved, and the
  branch behind it may now be passable.
- **A door that never opened.** A phrase flat at a few hundred a month for
  five years is a room whose demand never arrived. Cross-reference step 3:
  **a dead end whose vocabulary is still flat is a wall that is still a wall.**
  Two instruments agreeing is the strongest finding this run produces.
- **A vocabulary that migrated.** The same job renamed — the enterprise
  phrasing flat and expensive while a newer phrasing for the identical job
  climbs. The job did not change; the words the buyer uses did. Whoever still
  markets in the old words has a distribution problem they may not have
  noticed.

**The best room on the map is a proven dead end whose wall has since moved.**
Demand was proven, an attempt was made and dated, the reason it failed is
known, and that reason no longer holds. Nothing else combines evidence and
absence of competition the same way.

## 5. THE ROOMS — draw them from demand, not from companies

- `keyword_ideas` on 3–5 seeds taken from the JOB the category does, never
  from the category's name.
- `keyword_related` on the richest seed at `depth=2`. It traverses what the
  same people also search rather than what resembles your seed, which makes it
  the only instrument here that can leave the category you started in.
  Adjacent problems are adjacent rooms. Depth 3 and 4 leave the building.
- `keyword_overview` on everything pooled — one call, up to 700 terms, and it
  carries volume, intent and difficulty together. Past 700, `keyword_volume` and
  `keyword_intent` take 1,000 apiece.
- Read the difficulty column only for the commercial survivors, and only when
  search is a route you would actually enter through. That number is the cost of
  the door, not the value of the room.

**Fold your candidate category nouns into the same pool.** You need them in
step 8, and priced here they cost nothing extra.

**Check the harvest's centre of gravity before you price it.** Read the top of
the pool by volume times CPC. If it is another category's vocabulary — the
platform, the database, the department's tooling — your seeds were sector
nouns wearing a job's clothes, and the expansion followed the sector. Re-seed
from the sentence the buyer would say about their own problem, not from the
noun their industry uses for the activity.

**Srinivasan's acronym test, and this data can run half of it.** He argues the
businesses that worked were built on a constraint outsiders did not know —
know your customer for payments, laboratory developed tests for diagnostics,
the over-the-air reception rule for streaming television — and that you know
you have something when explaining the acronym sets off a light bulb. From
outside you can find the vocabulary, if not the constraint: terms the
incumbents rank for that your problem-led harvest never returned, and terms
carrying low volume with high CPC and commercial intent. Cheap words are
outsider words. **A term almost nobody searches that costs a fortune per click
is an insider term with a budget behind it**, and it is the likeliest place a
constraint worth knowing is hiding. The sharpest version carries all three at
once: tiny volume, a CPC larger than most products charge in a month, and a
high competition index — a handful of buyers a month that several advertisers
are fighting over. Go and learn the constraint before you
commit; this run can only point at it.

**A phrase that returns no row at all is not a small room.** Distinguish three
outcomes: measurable volume, a row reporting zero, and no row returned. The
last one means the phrase is not vocabulary — nobody shops in those words. Put
the feature your product leads with through this test by name. A headline
feature with no vocabulary is not necessarily a bad feature, but it cannot be
the thing you are found by, and pricing a room on it is pricing a room nobody
asks for.

Group into 5–8 rooms. Two terms belong in the same room when the same domains
rank for both; one `domain_serp_rivals` call on each of two candidate head
terms settles a boundary argument. Discard rooms with no commercial or
transactional intent — that is an audience, a different and harder business.
Use the floor demand-validation uses: about 5,000 searches a month for a
consumer room, about 1,000 for a B2B one.

## 6. OCCUPANCY — who is standing in each room

For the two or three largest domains on the roster:

- `domain_top_pages`. Does a page exist that is ABOUT this room, and does it
  earn traffic? A room covered in a paragraph on a feature page is not
  occupied. A room with its own page in their top ten is.
- `ads_creatives` with `target=<domain>`. Compute run length from
  `first_shown` and `last_shown`. **A creative live 90+ days is a claim that
  survived that company's own performance review**, and it outranks anything
  on their website. The `title` field is the advertiser's name, never the ad
  headline. The row count comes back capped, so report the median run length
  and the share running 90+ days rather than a creative count you cannot
  verify.
- `ads_meta_advertisers` on the room's own phrase, or on a competitor's
  domain. It searches ads BY PHRASE rather than by advertiser, so it returns
  companies absent from your roster — exactly who occupies a room you had
  scored as empty — and it names each one's `page_id` and dates their ads.
- `ads_meta_library` on that `page_id` for the creatives themselves. It
  answers as one image, because the copy in those ads is pixels: read it, or
  hand it to a vision model.

Score every room:

  OCCUPIED    a dedicated page in their top ten AND a creative sustained 90+ days
  CONTESTED   one of the two without the other
  OPEN        neither

Stated default rather than a measured constant: a room where incumbent pages
already rank for more than ~60% of its volume is occupied whatever the ads
say, and under ~20% it is open. Between the two you are fighting, not walking
in.

## 7. WATER OR DESERT — the test the whole run turns on

An OPEN room is a hypothesis. Three tests, cheapest first, and a room must
pass at least two:

1. **Money next door.** Free — you measured it in step 5. Do the room's
   commercial terms carry a real CPC? A room whose neighbours cost money to
   reach sits beside somebody's budget. A room where every CPC rounds to zero
   is being ignored by every advertiser who already tested it.
2. **Somebody is paid to do this today.** `company_jobs` on one listing for
   the role that does this job by hand — find the posting URL with your own
   search first. A salary band is a budget line that already exists, and the
   ceiling on what software can charge to remove it. The band itself is absent
   from most postings; the function being hired for is still a fact, and still
   costs them money.
3. **The nearest paid substitute.** `web_fetch` the closest incumbent's
   pricing page as `format=markdown`, or `format=html` when the tiers sit in a
   table you need cell by cell. Take the floor, the pushed tier, and what they
   meter on. The metering axis is the decision you will copy or break next.

**Whitespace with no money next to it is not whitespace. It is a market that
has already been priced, at zero.** Write that verdict per room and move on
rather than arguing with it.

**KILL CRITERION, fixed now:** if no room is both OPEN and passes two of the
three money tests, this maze has been walked. The remaining moves are price,
bundle, or a different maze — and reaching that is a result, not a failed run.
Report it with the rooms and the reason each one failed.

## 8. THE OFFER — five layers, decided together or not at all

Kim and Mauborgne's constraint governs this step: **an offer that only adds is
not a new position, it is a more expensive incumbent.** Their
eliminate-reduce-raise-create grid exists to force the half of the decision
that gets skipped, because subtracting is what makes a position both
defensible and cheap.

Fill five lines for the winning room. Each has to make the next obvious:

  POSITION   the branch you take, and the alternative you replace
  BUYER      the characteristic that makes someone a fit — a trigger, a scale,
             a constraint, a stack. Never a demographic
  BUNDLE     leaders behind the tier you want bought, fillers in the base tier
             where they raise perceived value at no cost, killers removed —
             Ramanujam's classification, worked properly in pricing-power
  PRICE      the metric first and the number second: say what the bill does
             when the customer succeeds
  MESSAGE    one sentence, in the buyer's own words, that the incumbent could
             not say

The message is evidence rather than copywriting. Take the phrasing from
`app_reviews` with `sort_by=most_recent` on an incumbent's app, or
`social_reddit_posts` on the room's canonical complaint thread. Quote
verbatim: a paraphrase loses the exact word the buyer would type, which is the
part you are buying.

Then run the three tests that kill most candidate offers:

- **THE SUBTRACTION TEST.** Name what you ELIMINATE and what you REDUCE, then
  name who will therefore not buy from you. An offer that eliminates nothing
  cannot be cheaper, faster or simpler than the incumbent, so it will be
  compared feature by feature — a comparison the incumbent wins by default.
- **THE SWAP TEST.** Put the incumbent's name at the top of your message. If
  it still reads true you have written the category's message, not yours, and
  the room is not open. Do it with the price and the bundle too: if their sales
  team could quote your bundle at your price tomorrow without changing their
  product, you have found a feature, not a position.
- **THE CLONE TEST.** An empty room is not a moat. Srinivasan's own examples
  are the winners who arrived second and executed faster — the search engines
  and social networks people remember are not the ones that got there first.
  So say how long the room stays yours once an incumbent notices, and what
  makes that longer than a quarter: the constraint from step 5, a distribution
  position, a data asset, a price they cannot match without hurting their
  existing book. "Nobody is there yet" is not on that list.

## 9. THE WALL YOU WILL HIT

From steps 3 and 4 you know who walked toward this room and what stopped them,
and whether that wall has moved. Name the wall on your own path and who hit it
first. If the answer is "nobody has tried this", either the map is incomplete
or the room is desert — both mean go back rather than forward.

Close with the cheapest experiment that would find your wall inside 30 days,
and the number it has to produce.

## Where this run is blind

- **A room with no query is invisible here.** The method is biased toward
  whitespace inside a vocabulary that already exists, and the largest new
  categories arrive before their words do. Two partial corrections sit in the
  run — the dead ends in step 3, where somebody tried it before the words
  existed, and step 4, where a vocabulary that migrated shows the words
  arriving. Neither is a substitute. Say so in the report.
- **The constraint itself is not public.** Step 5 can find the insider
  vocabulary; it cannot tell you the regulation, contract term or technical
  limit behind it. That part is practitioner knowledge and this API does not
  hold it.
- **Occupancy is measured in public search and public ads only.** A room held
  through a sales team, a channel partner, a procurement framework or an app
  store reads as empty here and is not. The cheap correction is hiring: a
  roster company staffing account executives against a room has occupied it in
  a way no page will show.
- **A domain is not a company.** Multi-product companies hold rooms on
  subdomains, on paths, and under brands sharing no domain with the anchor.
  Where the roster looks thin for a category you know is crowded, that is
  usually why.
- **An app-first product is nearly invisible to every step here.** A company
  whose product is downloaded rather than visited can carry real revenue and
  almost no ranked terms, and this run will read it as absent. When the anchor
  is one of those, the map is still worth drawing — anchor it on an incumbent
  per step 1 — but say plainly that the subject's own position was inferred
  from its site copy and its price, not measured.

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

The maze as a tree: the forks already run, who took each branch, and what
happened to them — dead ends named against the roster index, with what
`web_fetch` showed each one to be, and each wall marked still standing or
moved with the year it moved. Then the one room you would take, the five-line
offer that takes it, what that offer gives up, and how long it stays yours.
Then the wall you expect and who hit it first. State the strongest evidence
against your choice before you state the choice.

---

The same method is served as text at https://wutheringai.com/v1/free/skills/idea-maze, free and
without a token, and explained for a person at https://wutheringai.com/skills/idea-maze.
