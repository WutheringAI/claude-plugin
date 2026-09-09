---
name: market-data
description: >-
  Live market, competitor, advertising, app-store, company and web data from Wuthering AI:
  search demand and keyword volume, competitor domain traffic and rankings, live ad
  creatives and how long they have run, app listings and reviews, company funding and
  hiring, Reddit and LinkedIn posts, and live web search. Use this whenever a question
  needs current external evidence rather than training data — what a market is doing, who
  is advertising, what customers are complaining about, how big a company is — and
  whenever the user mentions Wuthering AI. Each successful call spends about 20¢ of the
  user's prepaid balance, so call deliberately. If the user already has a dedicated tool
  for that specific source, prefer it.
---

# Wuthering AI

One question, one URL, complete JSON back. There is nothing to install: this
plugin ships the caller, and the caller holds the credential.

## Connect

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --check
```

Exit 0 means connected. Anything else means run `/wuthering:connect`, which
walks the user through a device login and writes the token where these scripts
look for it. Never ask the user to paste a token into this conversation when the
login can fetch one itself.

## Call

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/call.mjs" --list
node "${CLAUDE_PLUGIN_ROOT}/scripts/call.mjs" web_search query="ai agent pricing"
node "${CLAUDE_PLUGIN_ROOT}/scripts/call.mjs" keyword_ideas keywords="ai agent" limit=50
```

- `--list` is free and prints every tool this deployment serves, with its
  parameters. Call nothing that is not on it — a guessed path is a 404.
- Array parameters are comma-separated: `keywords="ai agent,ai agents"`.
- `data` is the answer; `meta` carries what the call cost and what is left.
- The script exits non-zero on failure and prints what to do about it. Failed
  calls are not charged.

## The families

Paths are `<family>_<thing>`, and the family says what kind of question it
answers:

| family | what it answers |
|---|---|
| `keyword` | how many people search a term, what it costs, and whether it is growing |
| `domain` | what a competitor ranks for, what it earns from search, who it competes with |
| `ads` | who is advertising, on which platform, since when, and with what copy |
| `app` | app-store listings, rankings and reviews |
| `company` | size, funding, hiring, people |
| `social` | Reddit threads and comments, LinkedIn and Instagram posts, YouTube |
| `web` | live search, page fetch, screenshots, reading text out of an image |

## Before a run of more than three or four calls

Use one of the research skills in this plugin — demand validation, the
whitespace left in a category, positioning, pricing, channel choice, what to
build next, diligence on a company, or testing a belief the plan already rests
on. Each names the calls in order and carries the threshold that decides the
answer before the data arrives, which is what stops a run spending money on a
conclusion nobody can trust.

## Rules

1. Only call paths `--list` returned.
2. Every successful call spends the user's money. Say what a large run will cost
   before running it, and stop when a decision is reachable.
3. If a call is declined for lack of credit, stop and tell the user. Do not retry
   in a loop — the decline will not change until they top up at
   https://wutheringai.com/dashboard.
4. Present results as external evidence, kept separate from your own conclusions.
5. Coverage is public data. An empty result is not proof of an empty market; say
   so when it matters.

The full reference, including the parameters of every tool, is at https://wutheringai.com/v1
and https://wutheringai.com/skill.md. The research skills are free to read at
https://wutheringai.com/v1/free/skills, with or without an account.
