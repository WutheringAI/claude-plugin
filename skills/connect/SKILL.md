---
name: connect
description: >-
  Connect this agent to Wuthering AI so the other skills in this plugin can call it. Use
  when a skill reports that there is no token, when a call fails with an authentication
  error, when the user asks to sign in, log in, connect, or set up Wuthering AI, or when
  they ask whether their account is connected. Runs a device login: the user approves in a
  browser and the token is written to this plugin's own data directory, never into the
  conversation.
---

# Connect to Wuthering AI

## First, check whether this is needed

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --check
```

Exit 0 prints the connected account. Stop there and say so — a working
connection needs nothing further.

## Otherwise, log in

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --login
```

It prints a URL and an eight-character code, then waits. Show the user both,
exactly as printed, and tell them the code expires in fifteen minutes. Signing up
happens on that page if they have no account, and a new account starts with free
credit and no card.

The command exits when they approve. It writes the token to this plugin's data
directory with owner-only permissions, and prints the account it belongs to. The
token itself is never printed and must never be asked for: if the user offers to
paste one, they can, but do not request it.

## When it does not work

- **The code expired.** Codes last fifteen minutes. Run the login again rather
  than asking them to reuse the old code.
- **They denied it.** Stop. Ask what they would rather do; do not start another
  login unless they ask for one.
- **They have no account.** The same page signs them up. Free credit, no card.
- **It says connected but calls fail with 402.** That is credit, not
  authentication. They top up at https://wutheringai.com/dashboard.

## What this does not do

It does not ask for a password and never signs in on the user's behalf. The only
thing this agent does is start the flow, show the code, and wait.
