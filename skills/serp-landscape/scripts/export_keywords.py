#!/usr/bin/env python3
"""Flatten keywords.json into one self-contained row per keyword.

keywords.json is normalised: a keyword carries its cluster id, and the cluster
carries the size, head and intent mix. That is the right shape to compute
with and the wrong shape to hand to anyone else, because the interesting
signal -- how much demand sits behind this keyword -- lives one join away.

This writes every keyword with every signal already attached: where the
breadth-first search found it, what the ranking thought of it, what expanding
it returned, which topic it belongs to and how big that topic is, and, when
the SERPs have been captured and serp_metrics.py has run, what Google actually
answered it with.

Usage:
    python3 export_keywords.py --keywords keywords.json --out all_keywords.json
    python3 export_keywords.py --keywords keywords.json --metrics metrics.json \\
        --out all_keywords.json --csv all_keywords.csv
"""

import argparse
import csv
import json
import os

# Signals that come from serp_metrics.py. Absent until the SERPs are captured,
# so every one of them is optional and the export works on a fresh expansion.
METRIC_FIELDS = ["serp_intent", "intent_agrees", "serp_cluster", "demand_mass", "results",
                 "readable_results", "coverage_pct", "distinct_domains", "incumbent_share",
                 "median_word_count", "median_title_len", "median_desc_len",
                 "median_age_days", "share_listicle", "share_title_year", "kw_in_title"]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keywords", required=True, help="keywords.json from expand_keywords.py")
    ap.add_argument("--metrics", help="metrics.json from serp_metrics.py, if you have it")
    ap.add_argument("--out", required=True, help="where to write the flattened JSON")
    ap.add_argument("--csv", help="also write a CSV of the same rows")
    args = ap.parse_args()

    with open(args.keywords, encoding="utf-8") as fh:
        kw = json.load(fh)
    metrics = {}
    if args.metrics and os.path.exists(args.metrics):
        with open(args.metrics, encoding="utf-8") as fh:
            metrics = json.load(fh).get("keywords", {})

    clusters = {c["id"]: c for c in kw.get("clusters", [])}
    search = kw.get("search", {})
    rows = []
    for k in kw.get("keywords", []):
        cluster = clusters.get(k.get("cluster", ""), {})
        row = {
            "keyword": k["keyword"],
            # where the search found it
            "layer": k.get("level"),
            "found_via_probe": k.get("probe", ""),
            "source": k.get("source", ""),
            "suggest_rank": k.get("rank"),
            "suggest_relevance": k.get("relevance"),
            "seen_in_probes": k.get("seen_in_probes"),
            # what the search did with it
            "expanded": k.get("expanded", False),
            "children_found": k.get("children_found", 0),
            "expansion_score": k.get("expansion_score"),
            # the query itself
            "words": k.get("words"),
            "chars": k.get("chars"),
            "modifiers": k.get("modifiers", []),
            "is_question": k.get("is_question", False),
            "intent_prior": k.get("intent_prior", ""),
            # the topic it belongs to, joined in: demand mass without a lookup
            "topic_id": k.get("cluster", ""),
            "topic": cluster.get("label", ""),
            "topic_size": cluster.get("size"),
            "topic_head": cluster.get("head", ""),
            "topic_intent_prior": cluster.get("intent_prior", ""),
            "serp_sample": k.get("serp_sample", False),
        }
        m = metrics.get(k["keyword"], {})
        row["serp_captured"] = bool(m)
        for field in METRIC_FIELDS:
            row[field] = m.get(field)
        rows.append(row)

    payload = {
        "seed": kw.get("seed"),
        "locale": kw.get("locale"),
        "generated_at": kw.get("generated_at"),
        "guard_tokens": kw.get("must_include"),
        "target": kw.get("target"),
        "api_calls": kw.get("api_calls"),
        "sources": kw.get("sources"),
        # the search's own account of itself, so a reader can tell a small
        # topic from an abandoned search without rerunning anything
        "search": {"strategy": search.get("strategy"), "ranking": search.get("ranking"),
                   "frontier_fully_explored": search.get("frontier_fully_explored"),
                   "warnings": search.get("warnings", []),
                   "layers": search.get("layers", [])},
        "stats": kw.get("stats", {}),
        "serp_metrics_joined": bool(metrics),
        "keyword_count": len(rows),
        "keywords": rows,
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)

    if args.csv and rows:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
            writer.writeheader()
            for row in rows:
                writer.writerow({k: ("|".join(v) if isinstance(v, list) else v)
                                 for k, v in row.items()})

    print(json.dumps({"out": os.path.abspath(args.out),
                      "csv": os.path.abspath(args.csv) if args.csv else None,
                      "keywords": len(rows),
                      "fields_per_keyword": len(rows[0]) if rows else 0,
                      "serp_metrics_joined": bool(metrics)}, indent=2))


if __name__ == "__main__":
    main()
