#!/usr/bin/env python3
"""Grow one seed keyword into the thousands of queries people actually type.

Every keyword here comes from a live autocomplete API -- the same suggestion
list a searcher sees in the box -- so the set is a record of real demand rather
than a list you brainstormed. Provenance travels with each keyword (which probe
produced it, at what rank, with what relevance score), because a keyword nobody
can trace is a guess wearing a number.

Three things happen here:

  1. EXPAND   a breadth-first search over autocomplete. Layer 1 is the seed
              put through every probe shape -- question, commercial, relation,
              alphabet -- and it is always expanded in full, because it is the
              breadth every deeper layer inherits. Each layer after it is
              ranked by expansion_score, expanded in waves, and allowed to stop
              where it stops paying. A layer is finished before the next one
              begins, and keywords.json records each layer's frontier, how much
              of it was expanded, and why it stopped.
  2. CLUSTER  group the universe by shared wording, so you know how much demand
              sits behind each topic rather than treating 4,000 keywords as
              4,000 separate problems.
  3. SAMPLE   pick the keywords worth pulling a SERP for -- one representative
              per cluster, biggest clusters first. SERPs cost a search call
              each, so they are sampled; autocomplete is free, so it is not.

Four sources, and they are not interchangeable:

  google     client=chrome: 15 suggestions per call plus relevance scores
  youtube    the same API with ds=yt -- video-intent phrasing, ~50% different
  ddg        DuckDuckGo autocomplete, ~8 per call, mostly a subset of Google
  bing       Bing osjson, ~13 per call, mostly a subset of Google

Usage:
    python3 expand_keywords.py "espresso machine" --out keywords.json
    python3 expand_keywords.py "espresso machine" --target 10000 --sample 150
    python3 expand_keywords.py "cold email software" --sources google,youtube --locale en-GB
    python3 expand_keywords.py "cold email software" --must-include "cold email"
"""

import argparse
import concurrent.futures as futures
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

ENDPOINTS = {
    # client=chrome returns 15 with relevance scores; firefox returns 10 without.
    "google": "https://www.google.com/complete/search?client=chrome&hl={hl}&gl={gl}&q={q}",
    "youtube": "https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl={hl}&q={q}",
    "ddg": "https://duckduckgo.com/ac/?type=list&kl={kl}&q={q}",
    "bing": "https://www.bing.com/osjson.aspx?query={q}&mkt={mkt}",
}

# Suffix probes, grouped so the reason each exists is visible. Autocomplete
# completes a prefix, so every probe is "seed + something" -- the shape of the
# something decides which half of the market you get to see.
QUESTION_WORDS = ["how", "what", "why", "when", "which", "where", "who",
                  "is", "are", "can", "does", "do", "should", "will"]
COMMERCIAL_WORDS = ["best", "top", "cheap", "cheapest", "free", "price", "cost",
                    "buy", "review", "reviews", "alternative", "alternatives",
                    "vs", "versus", "comparison", "pricing", "discount", "deals",
                    "worth", "rated"]
RELATION_WORDS = ["for", "with", "without", "near", "like", "in", "on", "to",
                  "from", "under", "over", "and", "or", "that", "software",
                  "tool", "tools", "example", "examples", "template", "guide",
                  "checklist", "tips", "problems", "benefits", "types"]
LETTERS = list("abcdefghijklmnopqrstuvwxyz")

# Intent priors read off the wording. These are a starting guess only: what
# actually ranks decides intent, and serp_metrics.py overwrites this field once
# the SERPs are in. Keeping the prior visible makes the disagreements readable,
# and the disagreements are usually the interesting part.
INTENT_LEXICON = [
    ("transactional", r"\b(buy|order|shop|for sale|sale|purchase|coupon|discount|deal|deals|"
                      r"cheap|cheapest|price|prices|pricing|cost|near me|delivery|rent|"
                      r"subscription|trial|download|sign ?up|free|shipping|refurbished|used)\b"),
    ("commercial", r"\b(best|top|review|reviews|rating|ratings|compare|comparison|vs|versus|"
                   r"alternative|alternatives|competitor|competitors|worth|which|"
                   r"recommended|ranked|leading|brands?|rated)\b"),
    ("navigational", r"\b(login|log in|sign in|website|customer service|support|"
                     r"contact|careers|dashboard|portal|account|manual|warranty)\b"),
    ("informational", r"\b(how|what|why|when|guide|tutorial|examples?|meaning|definition|"
                      r"ideas|tips|checklist|template|explained|difference|does|do|"
                      r"can|steps|learn|beginners?|problems?|benefits|types|parts|repair|"
                      r"clean|fix|maintenance|settings|instructions)\b"),
]

STOP = set("a an the and or of for to in on at by with without is are be as from that this "
           "your you my our it its how what why when which where who do does can should will "
           "not no near me best top vs versus".split())


def log(msg, quiet=False):
    if not quiet:
        print(msg, file=sys.stderr, flush=True)


def norm(text):
    return re.sub(r"\s+", " ", str(text or "")).strip().lower()


def tokens(text):
    return re.findall(r"[a-z0-9']+", str(text or "").lower())


def core_tokens(seed):
    toks = [t for t in tokens(seed) if t not in STOP and len(t) > 2]
    return toks or tokens(seed)


# Head nouns that name the category rather than the subject. These are the
# words autocomplete swaps most freely -- "cold email software" completes to
# "cold email tool", "cold email platform", "cold email client" -- and they are
# very often the longest word in the seed, so anchoring on length pins the
# whole universe to the one token searchers vary most and throws the topic
# away. Anchor on what is left of the seed instead.
GENERIC_HEAD = set("""software tool tools app apps application applications platform platforms
service services system systems solution solutions program programs suite suites product
products machine machines device devices company companies vendor vendors provider providers
agency agencies website websites site sites page pages online management manager taking maker
makers builder builders generator generators tracker trackers checker checkers analyzer
analyser dashboard portal engine engines""".split())


def required_tokens(seed):
    """Tokens that keep a suggestion on-topic -- at least one must survive.

    Autocomplete happily walks away from your seed ("how espresso machine"
    completes to "how coffee machine"), so a drift guard is worth having. The
    guard has to hold onto what makes the seed *this* topic, which is the part
    that is not the category noun: "espresso", not "machine"; "cold email", not
    "software". Requiring any one of those keeps the legitimate long tail --
    which rarely repeats every word of the seed -- while still dropping
    suggestions that have wandered into a different subject.

    A seed that is nothing but category nouns ("project management software")
    falls back to its own content tokens, because some guard beats none.
    """
    toks = core_tokens(seed)
    distinctive = [t for t in toks if t not in GENERIC_HEAD]
    return distinctive or toks or [seed.lower()]


def intent_prior(keyword):
    low = " %s " % norm(keyword)
    for label, pattern in INTENT_LEXICON:
        if re.search(pattern, low):
            return label
    return "unclassified"


def modifiers(keyword, seed_tokens):
    """Words this keyword adds to the seed -- the reason it is a distinct query."""
    return [t for t in tokens(keyword) if t not in seed_tokens and t not in STOP][:8]


class Suggest:
    """Autocomplete client that slows down instead of hammering a rate limit."""

    def __init__(self, locale="en-US", delay=0.12, timeout=12):
        lang, _, region = locale.partition("-")
        self.hl = lang or "en"
        self.gl = (region or "us").lower()
        self.kl = "%s-%s" % (self.gl, self.hl)
        self.mkt = "%s-%s" % (self.hl, self.gl.upper())
        self.delay = delay
        self.timeout = timeout
        self.calls = 0
        self.failures = []
        self._lock = threading.Lock()
        self._recent_fail = 0

    def _url(self, source, query):
        return ENDPOINTS[source].format(q=urllib.parse.quote_plus(query), hl=self.hl,
                                        gl=self.gl, kl=self.kl, mkt=self.mkt)

    def _note(self, ok, msg=""):
        with self._lock:
            if ok:
                self.calls += 1
                self._recent_fail = max(0, self._recent_fail - 1)
            else:
                self._recent_fail += 1
                if len(self.failures) < 40:
                    self.failures.append(msg)
                # Backing off beats getting cut off mid-run.
                if self._recent_fail and self._recent_fail % 5 == 0:
                    self.delay = min(1.5, self.delay * 1.6)

    def fetch(self, source, query):
        """Return [(suggestion, rank, relevance)]. Never raises: a dead probe is a gap."""
        url = self._url(source, query)
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        body = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = resp.read(400_000).decode("utf-8", errors="replace")
                self._note(True)
                break
            except Exception as e:                        # noqa: BLE001
                if attempt == 2:
                    self._note(False, "%s %r: %s" % (source, query, type(e).__name__))
                    return []
                time.sleep(0.5 * (attempt + 1) ** 2)
        # Some endpoints wrap the array in a JSONP callback.
        body = re.sub(r"^[^\[\{]*\(", "", (body or "").strip()).rstrip(");")
        try:
            data = json.loads(body)
        except Exception:                                 # noqa: BLE001
            self._note(False, "%s %r: unparseable body" % (source, query))
            return []
        if not isinstance(data, list) or len(data) < 2 or not isinstance(data[1], list):
            return []
        scores = []
        for item in data[2:]:
            if isinstance(item, dict) and "google:suggestrelevance" in item:
                scores = item["google:suggestrelevance"]
        out = []
        for i, entry in enumerate(data[1]):
            text = entry[0] if isinstance(entry, (list, tuple)) and entry else entry
            if isinstance(text, str) and text.strip():
                rel = scores[i] if i < len(scores) and isinstance(scores[i], (int, float)) else None
                out.append((norm(text), i + 1, rel))
        time.sleep(self.delay)
        return out


def seed_probes(seed, letters=True, digits=False):
    """Prefixes to complete at level 1. Order matters: the plain seed first,
    then the modifier families, then the alphabet -- so a run cut short still
    has the high-value shapes rather than 'seed a' through 'seed f'."""
    out = [seed]
    out += ["%s %s" % (w, seed) for w in QUESTION_WORDS]
    out += ["%s %s" % (seed, w) for w in COMMERCIAL_WORDS]
    out += ["%s %s" % (w, seed) for w in ("best", "top", "cheap", "free", "buy")]
    out += ["%s %s" % (seed, w) for w in RELATION_WORDS]
    if letters:
        out += ["%s %s" % (seed, c) for c in LETTERS]
    if digits:
        out += ["%s %s" % (seed, d) for d in "0123456789"]
    return list(dict.fromkeys(out))


def harvest(sug, sources, queries, workers=8):
    """Run one wave of probes, parallel across probes and sources."""
    jobs = [(s, q) for q in queries for s in sources]
    out = []

    def one(job):
        source, q = job
        return source, q, sug.fetch(source, q)

    with futures.ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        for source, q, hits in pool.map(one, jobs):
            out.append((source, q, hits))
    return out


# ------------------------------------------------------------------ ranking

# What the expansion score is made of, and why each part earns its weight.
# Exposed in keywords.json as `expansion_score` so the order a run chose can be
# audited rather than taken on trust.
SCORE_WEIGHTS = {
    "relevance": 0.34,      # Google's own suggestrelevance for the node
    "rank": 0.14,           # where it sat in the suggestion list
    "corroboration": 0.16,  # how many different probes returned it: a hub, not a leaf
    "headroom": 0.21,       # short queries have room to complete; a 12-word one does not
    "parentage": 0.15,      # its parent probe was productive, so siblings likely are
}


def expansion_score(entry, max_relevance, parent_yield):
    """How much unexplored breadth probably sits under this keyword.

    Autocomplete completes a prefix, so expanding a node returns what people
    type *after* it. That makes "worth expanding" a different question from
    "important keyword": a long, highly specific query can be a fine keyword
    and a dead end as a probe, because there is nothing left to append. The
    score below is about breadth still available, not about the keyword's own
    value -- which is why headroom carries almost as much weight as relevance.
    """
    rel = (entry.get("relevance") or 0) / max_relevance if max_relevance else 0.0
    rank = 1.0 / (1.0 + max(0, entry.get("rank") or 0))
    corroboration = min(entry.get("seen_in_probes", 1), 5) / 5.0
    headroom = max(0.0, (12 - entry.get("words", 1)) / 11.0)
    w = SCORE_WEIGHTS
    return round(w["relevance"] * rel + w["rank"] * rank
                 + w["corroboration"] * corroboration + w["headroom"] * headroom
                 + w["parentage"] * parent_yield, 4)


def order_frontier(entries, scores):
    """Rank a whole layer for expansion, without digging one hole.

    Score order alone would expand fifty phrasings of one sub-topic before
    touching another, so a layer cut short would come back lopsided. Bucketing
    by each node's leading modifier and rotating through the buckets -- best
    node from each, biggest bucket first -- spends the layer across the market
    instead. A layer expanded to exhaustion ends up with the same set either
    way; this only decides the order, which is what matters when a deeper layer
    stops early.
    """
    buckets = defaultdict(list)
    for e in sorted(entries, key=lambda e: (-scores.get(e["keyword"], 0.0), e["chars"])):
        buckets[e["modifiers"][0] if e["modifiers"] else "_seed"].append(e)
    order = []
    while True:
        live = [s for s in buckets if buckets[s]]
        if not live:
            return order
        for shape in sorted(live, key=lambda s: -len(buckets[s])):
            if buckets[shape]:
                order.append(buckets[shape].pop(0)["keyword"])


# ---------------------------------------------------------------- clustering

# Words that describe HOW someone is searching rather than WHAT they are
# searching about. "best espresso machine for home" is about home machines; the
# "best" is intent. Letting intent words anchor a topic produces one enormous
# "best" cluster and tells you nothing about the market.
GENERIC = set("""best top cheap cheapest free price prices pricing cost costs buy sale sales
deal deals discount review reviews rating ratings rated compare comparison versus alternative
alternatives 2023 2024 2025 2026 2027 reddit youtube quora amazon walmart ebay costco guide
guides tutorial worth good better great new used refurbished online shop store shops stores
list ranked recommended tips ideas need needs make makes making get gets buying""".split())


def cluster_by_topic(entries, seed_tokens, df_ceiling=0.05):
    """Group the universe into topics, so demand has a shape you can weigh.

    Each keyword is filed under its most-shared substantive word: "espresso
    machine with grinder" and "does espresso machine come with grinder" both
    land under `grinder`. Two guards make that work. Intent words are barred
    from anchoring, or half the market files under "best". And a word used by
    more than `df_ceiling` of the corpus is barred too -- a near-synonym of the
    seed ("coffee" here) otherwise swallows a fifth of the keywords into one
    cluster that means nothing.

    This is the cheap pass, run before a single SERP exists, which is what
    makes sampling possible. It groups by wording, and wording is a proxy for
    intent rather than a substitute: two keywords sharing no words can still
    share a SERP. serp_metrics.py regroups the sampled keywords by the URLs
    Google actually returns, and where the two disagree, Google wins.
    """
    def content(keyword):
        return [t for t in tokens(keyword) if t not in STOP and t not in seed_tokens]

    df = Counter()
    for e in entries:
        df.update(set(content(e["keyword"])))
    cap = max(3, len(entries) * df_ceiling)

    groups = defaultdict(list)
    for e in entries:
        toks = content(e["keyword"])
        substantive = [t for t in toks if t not in GENERIC and len(t) > 2]
        pool = [t for t in substantive if df[t] <= cap] or substantive \
            or [t for t in toks if len(t) > 2] or toks
        anchor = max(pool, key=lambda t: (df[t], -len(t))) if pool else "_seed"
        groups[anchor].append(e["keyword"])
    return groups


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("seed", help="the seed keyword, e.g. \"espresso machine\"")
    ap.add_argument("--target", type=int, default=5000,
                    help="keywords to keep in the universe (default 5000; raise freely, "
                         "autocomplete is cheap)")
    ap.add_argument("--sample", type=int, default=100,
                    help="keywords marked for SERP capture (default 100). Each one costs a "
                         "web search, so this is the number that decides run length")
    ap.add_argument("--out", default="keywords.json")
    ap.add_argument("--locale", default="en-US", help="language-REGION, e.g. en-GB, de-DE")
    ap.add_argument("--sources", default="google",
                    help="comma-separated: google,youtube,ddg,bing (default google)")
    ap.add_argument("--depth", type=int, default=6,
                    help="deepest layer to reach (default 6). 1 is the seed's own probes and "
                         "nothing else. Layers stop early once --target is met or the frontier "
                         "runs dry, so this is a ceiling rather than a plan")
    ap.add_argument("--branch", type=int, default=1500,
                    help="most nodes expanded in any one layer BELOW layer 1 (default 1500). "
                         "Layer 1 is always expanded in full, because it is the breadth every "
                         "deeper layer inherits")
    ap.add_argument("--wave", type=int, default=150,
                    help="nodes probed per wave inside a layer (default 150). Yield is measured "
                         "per wave, so this is the granularity at which a layer can stop early")
    ap.add_argument("--min-yield", type=float, default=0.6,
                    help="new keywords per probe below which a layer below layer 1 stops "
                         "(default 0.6). Lower it to keep digging a thin topic")
    ap.add_argument("--extra", default="",
                    help="comma-separated keywords you found elsewhere (related searches, "
                         "People Also Ask); kept verbatim with source=manual")
    ap.add_argument("--extra-file", help="file with one such keyword per line")
    ap.add_argument("--must-include", default="",
                    help="comma-separated tokens; a keyword is kept if it contains any one of "
                         "them (default: the seed's own tokens minus category nouns like "
                         "'software' or 'platform'). Pass '-' to keep everything autocomplete "
                         "returns.")
    ap.add_argument("--df-ceiling", type=float, default=0.05,
                    help="a word used by more than this share of the universe cannot anchor a "
                         "topic (default 0.05) -- it stops a near-synonym of the seed from "
                         "swallowing a fifth of the keywords into one meaningless cluster")
    ap.add_argument("--no-letters", action="store_true", help="skip the a-z alphabet soup")
    ap.add_argument("--digits", action="store_true", help="also probe seed + 0-9")
    ap.add_argument("--delay", type=float, default=0.12)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    seed = norm(args.seed)
    seed_tokens = set(tokens(seed))
    sources = [s.strip() for s in args.sources.split(",") if s.strip() in ENDPOINTS]
    if not sources:
        raise SystemExit("no valid --sources; choose from %s" % ", ".join(ENDPOINTS))
    if args.must_include == "-":
        required = []
    elif args.must_include.strip():
        required = [norm(t) for t in args.must_include.split(",") if norm(t)]
    else:
        required = required_tokens(seed)

    sug = Suggest(args.locale, args.delay)
    keywords, dropped = {}, []
    t0 = time.time()

    def add(text, level, source, probe, rank, relevance):
        key = norm(text)
        if not key or (key == seed and level > 0):
            return
        if required and not any(t in key for t in required):
            dropped.append({"keyword": key, "probe": probe,
                            "reason": "drifted off-topic: has none of %s"
                                      % ", ".join(repr(t) for t in required)})
            return
        if len(key) > 140 or len(key.split()) > 14:
            dropped.append({"keyword": key, "probe": probe, "reason": "too long to be a query"})
            return
        prior = keywords.get(key)
        if prior:
            prior["seen_in_probes"] += 1
            # Breadth-first, so the first sighting is the shallowest one and the
            # layer a keyword is filed under is its true distance from the seed.
            # Only a better rank within the same layer can revise the provenance.
            if (level, rank) < (prior["level"], prior["rank"]):
                prior.update(level=level, source=source, probe=probe, rank=rank)
            if relevance and (prior.get("relevance") or 0) < relevance:
                prior["relevance"] = relevance
            return
        keywords[key] = {
            "keyword": key, "level": level, "source": source, "probe": probe,
            "rank": rank, "relevance": relevance, "seen_in_probes": 1,
            "words": len(key.split()), "chars": len(key),
            "modifiers": modifiers(key, seed_tokens), "intent_prior": intent_prior(key),
            "is_question": bool(re.match(r"^(how|what|why|when|which|where|who|is|are|can|"
                                         r"does|do|should|will)\b", key)),
            # BFS bookkeeping: was this node itself expanded, what did expanding
            # it return, and what did the ranking think of it beforehand.
            "expanded": False, "children_found": 0, "expansion_score": None,
        }

    add(seed, 0, "seed", "seed", 0, None)

    def expand(queries, layer, layers_seen):
        """Probe a set of queries and file everything they return into `layer`.

        Returns how many keywords were new, and credits each probed node with
        the children it produced, which is what `parentage` scores next layer.
        """
        gained = 0
        for source, probe, hits in harvest(sug, sources, queries, args.workers):
            before = len(keywords)
            for text, rank, rel in hits:
                add(text, layer, "%s:suggest" % source, probe, rank, rel)
            found = len(keywords) - before
            gained += found
            node = keywords.get(probe)
            if node is not None:
                node["children_found"] = node.get("children_found", 0) + found
                node["expanded"] = True
        layers_seen.update(queries)
        return gained

    # -- layer 1: complete the seed's own frontier --------------------------
    wave = seed_probes(seed, letters=not args.no_letters, digits=args.digits)
    log("layer 1: %d seed probes x %d source(s)" % (len(wave), len(sources)), args.quiet)
    probed = {seed}
    t_layer = time.time()
    expand(wave, 1, probed)
    layers = [{"layer": 1, "from_layer": 0, "discovered": len(keywords) - 1,
               "frontier": 1, "expanded": 1,
               "probes": len(wave) * len(sources), "policy": "exhaustive",
               "stopped_because": "seed probe shapes exhausted",
               "seconds": round(time.time() - t_layer, 1)}]
    log("  -> %d keywords (%.0fs)" % (len(keywords), time.time() - t0), args.quiet)

    # -- breadth-first from there ------------------------------------------
    # One layer at a time, and a layer is finished before the next one starts.
    # That ordering is the point: a keyword two completions from the seed is a
    # different kind of query from one five completions out, and mixing them
    # means a run cut short has explored neither properly. Layer 1 is always
    # expanded to exhaustion, because it is the breadth every later layer
    # inherits -- leave a layer-1 node unprobed and the whole subtree under it
    # is missing from the universe with nothing to show that it ever existed.
    #
    # Deeper layers are ranked by expansion_score and expanded in waves, so a
    # layer can stop where it stops paying rather than at a fixed budget. What
    # a layer did, and why it stopped, is recorded in `layers` for audit.
    for src_layer in range(1, max(1, args.depth)):
        if len(keywords) >= args.target:
            log("layer %d: not expanded, universe already at target (%d)"
                % (src_layer, len(keywords)), args.quiet)
            break
        frontier = [k for k in keywords.values()
                    if k["level"] == src_layer and k["keyword"] not in probed]
        if not frontier:
            log("layer %d: empty, nothing left to expand" % src_layer, args.quiet)
            break

        max_rel = max((e.get("relevance") or 0) for e in frontier)
        max_children = max([keywords[e["probe"]].get("children_found", 0)
                            for e in frontier if e["probe"] in keywords] or [0])
        scores = {}
        for e in frontier:
            parent = keywords.get(e["probe"])
            parent_yield = ((parent.get("children_found", 0) / max_children)
                            if parent and max_children else 1.0)
            e["expansion_score"] = expansion_score(e, max_rel, parent_yield)
            scores[e["keyword"]] = e["expansion_score"]
        order = order_frontier(frontier, scores)

        # Layer 1 is exhaustive by design. A deeper layer gets its whole frontier
        # ranked and then spends up to --branch of it, stopping sooner when the
        # wave loop below sees --target met or the yield collapse.
        exhaustive = src_layer == 1
        budget = len(order) if exhaustive else min(len(order), args.branch)
        t_layer, spent, gained_total = time.time(), 0, 0
        stopped = "layer exhausted"
        log("layer %d -> %d: %d nodes on the frontier, expanding %s"
            % (src_layer, src_layer + 1, len(order),
               "all of them" if exhaustive else "up to %d" % budget), args.quiet)

        while spent < budget:
            if len(keywords) >= args.target:
                stopped = "target reached"
                break
            # Clamped to the budget, not just sized by --wave: an unclamped
            # final wave overshoots a --branch cap by up to a whole wave.
            chunk = order[spent: min(spent + args.wave, budget)]
            gained = expand(chunk, src_layer + 1, probed)
            spent += len(chunk)
            gained_total += gained
            rate = gained / float(len(chunk))
            log("    %d/%d probed, +%d (%.1f new per probe), %d keywords (%.0fs)"
                % (spent, budget, gained, rate, len(keywords), time.time() - t0), args.quiet)
            # A topic with 800 real queries in it should not grind through every
            # remaining node to prove it -- but only a deeper layer may give up,
            # because layer 1 decides the breadth of everything below it.
            if not exhaustive and rate < args.min_yield:
                stopped = "yield %.1f fell below --min-yield %.1f" % (rate, args.min_yield)
                break
        else:
            if not exhaustive and spent < len(order):
                stopped = "--branch cap of %d reached" % args.branch

        # "layer 3, from_layer 2, expanded 266 of a 266-node frontier" reads as
        # one sentence: which layer this produced, and how much of the layer
        # below it was opened to produce it.
        layers.append({"layer": src_layer + 1, "from_layer": src_layer,
                       "discovered": gained_total,
                       "frontier": len(order), "expanded": spent,
                       "probes": spent * len(sources),
                       # the rule the layer ran under; stopped_because is what
                       # actually happened, and a ranked layer may still exhaust
                       "policy": "exhaustive" if exhaustive else "ranked",
                       "stopped_because": stopped,
                       "seconds": round(time.time() - t_layer, 1)})
        log("  layer %d done: +%d keywords from %d nodes (%s)"
            % (src_layer + 1, gained_total, spent, stopped), args.quiet)

    # -- keywords you brought yourself -------------------------------------
    manual = [k.strip() for k in args.extra.split(",") if k.strip()]
    if args.extra_file and os.path.exists(args.extra_file):
        with open(args.extra_file, encoding="utf-8") as fh:
            manual += [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
    for text in manual:
        key = norm(text)
        if key in keywords:
            keywords[key]["source"] += "+manual"
            continue
        keywords[key] = {"keyword": key, "level": 1, "source": "manual", "probe": "supplied",
                         "rank": 0, "relevance": None, "seen_in_probes": 1,
                         "words": len(key.split()), "chars": len(key),
                         "modifiers": modifiers(key, seed_tokens), "intent_prior": intent_prior(key),
                         "is_question": False,
                         "expanded": False, "children_found": 0, "expansion_score": None}

    # -- trim to --target, keeping the depth ------------------------------
    # Sorting by layer would put every deep keyword last and a target smaller
    # than the universe would then quietly throw away the whole point of
    # digging. Quotas keep each layer's share of the set -- and layer 1 is kept
    # whole, because it was expanded exhaustively to establish the breadth and
    # trimming it would throw that away at the last step.
    pool = list(keywords.values())
    if len(pool) > args.target:
        share = {0: 1.0, 1: 1.0, 2: 0.35, 3: 0.25, 4: 0.20, 5: 0.15}
        by_level = defaultdict(list)
        for k in pool:
            by_level[k["level"]].append(k)
        chosen = []
        for level in sorted(by_level):
            group = sorted(by_level[level],
                           key=lambda k: (-(k["relevance"] or 0), -k["seen_in_probes"],
                                          k["rank"], k["chars"]))
            quota = 1 if level == 0 else int(args.target * share.get(level, 0.15))
            chosen += group[:quota]
        if len(chosen) < args.target:
            taken = {c["keyword"] for c in chosen}
            rest = sorted((k for k in pool if k["keyword"] not in taken),
                          key=lambda k: (-(k["relevance"] or 0), k["rank"]))
            chosen += rest[: args.target - len(chosen)]
        pool = chosen[: args.target]

    # -- cluster the universe ---------------------------------------------
    groups = cluster_by_topic(pool, seed_tokens, args.df_ceiling)
    by_kw = {k["keyword"]: k for k in pool}
    clusters = []
    for anchor, members in sorted(groups.items(), key=lambda g: -len(g[1])):
        members.sort(key=lambda kw: (-(by_kw[kw]["relevance"] or 0), by_kw[kw]["rank"],
                                     by_kw[kw]["chars"]))
        cid = "c%03d" % (len(clusters) + 1)
        intents = Counter(by_kw[m]["intent_prior"] for m in members)
        clusters.append({"id": cid, "label": anchor, "head": members[0],
                         "size": len(members), "members": members,
                         "questions": sum(1 for m in members if by_kw[m]["is_question"]),
                         "intent_prior": intents.most_common(1)[0][0],
                         "intent_mix": dict(intents.most_common())})
        for m in members:
            by_kw[m]["cluster"] = cid

    # -- choose the SERP sample -------------------------------------------
    # One representative per cluster, biggest cluster first: that way the
    # searches you spend are spread across the demand rather than piled onto
    # ten phrasings of the same question. Each sampled keyword carries its
    # cluster size, so the map can weight a dot by the demand behind it.
    sample, round_no = [], 0
    while len(sample) < args.sample and round_no < 12:
        added = False
        for cluster in clusters:
            if round_no < len(cluster["members"]):
                sample.append(cluster["members"][round_no])
                added = True
                if len(sample) >= args.sample:
                    break
        if not added:
            break
        round_no += 1
    if seed in by_kw and seed not in sample:
        sample.insert(0, seed)
        sample = sample[: max(1, args.sample)]
    sample_set = set(sample)
    for k in pool:
        k["serp_sample"] = k["keyword"] in sample_set

    by_intent, by_level_count = Counter(), Counter()
    for k in pool:
        by_intent[k["intent_prior"]] += 1
        by_level_count[k["level"]] += 1

    # Every layer's frontier size, how much of it was expanded, and why it
    # stopped. This is the record that says whether a short universe means the
    # topic is small or means the search gave up -- which is the difference
    # between a finding and a gap.
    complete = all(ly.get("stopped_because") in ("layer exhausted",
                                                 "seed probe shapes exhausted")
                   for ly in layers)
    payload = {
        "seed": seed, "locale": args.locale, "sources": sources, "depth": args.depth,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        # must_include is the token set; a keyword holding any one of them was kept.
        "target": args.target, "sample_size": len(sample), "must_include": required or None,
        "api_calls": sug.calls, "elapsed_seconds": round(time.time() - t0, 1),
        "search": {"strategy": "breadth-first",
                   "ranking": SCORE_WEIGHTS,
                   "layer1_exhaustive": True,
                   "min_yield": args.min_yield, "wave": args.wave,
                   "branch_cap": args.branch,
                   "frontier_fully_explored": complete,
                   "layers": layers},
        "stats": {"discovered": len(keywords), "kept": len(pool),
                  "clusters": len(clusters), "dropped_off_topic": len(dropped),
                  "by_level": dict(sorted(by_level_count.items())),
                  "by_intent_prior": dict(by_intent.most_common()),
                  "probe_failures": sug.failures[:10]},
        "clusters": [{k: v for k, v in c.items() if k != "members"} | {"members": c["members"][:40]}
                     for c in clusters],
        "keywords": pool,
        "dropped": dropped[:80],
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    base = os.path.splitext(args.out)[0]
    with open(base + ".txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(k["keyword"] for k in pool) + "\n")
    targets = base.replace("keywords", "serp_targets") if "keywords" in base else base + "_serp"
    with open(targets + ".txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(sample) + "\n")

    print(json.dumps({"out": os.path.abspath(args.out),
                      "universe_list": os.path.abspath(base + ".txt"),
                      "serp_targets": os.path.abspath(targets + ".txt"),
                      "discovered": len(keywords), "kept": len(pool),
                      "clusters": len(clusters), "serp_sample": len(sample),
                      "api_calls": sug.calls, "seconds": payload["elapsed_seconds"],
                      "by_level": payload["stats"]["by_level"],
                      "by_intent_prior": payload["stats"]["by_intent_prior"],
                      "dropped_off_topic": len(dropped),
                      "frontier_fully_explored": complete,
                      "layers": [{"layer": ly["layer"], "discovered": ly["discovered"],
                                  "expanded": "%s of %s nodes in layer %s"
                                              % (ly["expanded"], ly["frontier"],
                                                 ly["from_layer"]),
                                  "stopped_because": ly["stopped_because"]}
                                 for ly in layers],
                      "probe_failures": len(sug.failures)}, indent=2))


if __name__ == "__main__":
    main()
