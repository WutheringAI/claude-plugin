# Wuthering AI for Claude Code

Live market, competitor, advertising, app-store, company and web data — and the
research methods that decide which calls are worth making.

```
/plugin marketplace add WutheringAI/claude-plugin
/plugin install wuthering@wutheringai
```

Then, in Claude Code:

```
/wuthering:connect                 sign in (or sign up — $5 of credit, no card)
/wuthering:demand-validation an AI scribe for private-practice therapists
```

## What is in it

**Two skills for the data itself.**

| skill | what it does |
|---|---|
| `/wuthering:connect` | device login. The token is written to the plugin's data directory, never into the conversation |
| `/wuthering:market-data` | how to call the API: 56 tools, one GET each, complete JSON back |

**Eight research methods**, each one a skill that names the calls in order, the
evidence that outranks other evidence, and the threshold that decides the answer
before the data arrives:

`/wuthering:demand-validation` · `/wuthering:idea-maze` ·
`/wuthering:positioning-teardown` · `/wuthering:pricing-power` ·
`/wuthering:channel-bet` · `/wuthering:switch-evidence` ·
`/wuthering:company-diligence` · `/wuthering:crucial-test`

**Two desk-research skills** that spend nothing and run entirely on this
machine plus your own web search:

| skill | what it does |
|---|---|
| `/wuthering:competitor-landscape` | maps the market two levels out from one company, out of the words those companies use to sell themselves. Excel workbook and 2×2 maps |
| `/wuthering:serp-landscape` | one seed keyword becomes thousands of real autocomplete queries, a sample of their search results, and every ranking page read for title, headings, length and freshness |

Both are free to run. They ask for a Wuthering AI account so we know who is
running them, which is the same account the paid tools use.

## What it costs

Reading the eight research methods is free, with or without an account — they
are served at <https://wutheringai.com/v1/free/skills> and always will be.

Data calls are 20¢ each, charged only when a call succeeds, from a prepaid
balance. A new account starts with $5 and no card. A disciplined research run is
9 to 18 calls, and every skill states its own budget before it starts.

## How the credential is handled

`scripts/login.mjs` runs a device login: it prints a URL and an eight-character
code, you approve in a browser, and it writes the token to
`${CLAUDE_PLUGIN_DATA}/token` with owner-only permissions.

`scripts/call.mjs` reads it from there and puts it in a header. **The token is
never printed, never an argument, and never in a URL** — an agent that pastes a
credential into a shell command has written it into a transcript that will be
stored and probably summarised somewhere else.

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --check     # connected?
node "${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --login     # connect
node "${CLAUDE_PLUGIN_ROOT}/scripts/call.mjs" --list       # every tool, free
node "${CLAUDE_PLUGIN_ROOT}/scripts/call.mjs" web_search query="ai agent pricing"
```

Set `WUTHERING_TOKEN` to override the saved token, and `WUTHERING_ORIGIN` to
point at another deployment.

## Where this comes from

Everything except the two desk-research skills is **generated** from the
Wuthering AI monorepo, from the same catalogue that serves the API — so a skill
cannot name a tool that no longer exists, and a stated price cannot drift from
the one charged. Regenerate with `pnpm run build:plugin`; `verify-plugin` fails
the build when what is committed stops matching.

`competitor-landscape` and `serp-landscape` are vendored from
[samsam32118/desk-research-](https://github.com/samsam32118/desk-research-),
unchanged except for a sign-in check at the top and `$SKILL` bound to
`${CLAUDE_SKILL_DIR}`.

## Requirements

Node 18 or newer for the two scripts. The desk-research skills additionally need
Python 3 with `openpyxl`; each states its own requirements.

MIT licensed.
