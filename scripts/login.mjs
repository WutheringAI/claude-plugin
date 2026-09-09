#!/usr/bin/env node
/**
 * Connect this machine to Wuthering AI, and check whether it already is.
 *
 *   node login.mjs --check     is there a working token? exit 0 if yes
 *   node login.mjs --login     run the device login and save one
 *   node login.mjs --logout    forget the saved token
 *
 * The token is written to the plugin's own data directory rather than printed.
 * An agent that prints a credential has published it: the transcript is stored,
 * summarised, and often shared. So the login writes the file and says who it
 * belongs to, and `call.mjs` reads it back without it ever passing through the
 * conversation.
 *
 * Zero dependencies on purpose. This has to run wherever the plugin is
 * installed, before anything has been set up, on whatever Node is present.
 */
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const ORIGIN = process.env['WUTHERING_ORIGIN'] ?? 'https://wutheringai.com';

/**
 * Where the credential lives.
 *
 * `CLAUDE_PLUGIN_DATA` survives plugin updates, which is what a credential
 * needs — the version directory changes underneath it on every upgrade. The
 * fallback is for running these scripts by hand, outside a plugin.
 */
export function tokenPath() {
  const dir = process.env['CLAUDE_PLUGIN_DATA'] ?? path.join(homedir(), '.wuthering');
  return path.join(dir, 'token');
}

export function readToken() {
  const fromEnv = process.env['WUTHERING_TOKEN']?.trim();
  if (fromEnv) return fromEnv;
  const file = tokenPath();
  if (!existsSync(file)) return null;
  const value = readFileSync(file, 'utf8').trim();
  return value.length > 0 ? value : null;
}

function saveToken(token) {
  const file = tokenPath();
  mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  writeFileSync(file, `${token}\n`, { mode: 0o600 });
  return file;
}

/** Who a token belongs to, or null if it is not a working token. */
export async function whoami(token) {
  const response = await fetch(new URL('/api/cli/whoami', ORIGIN), {
    headers: { authorization: `Bearer ${token}` },
  });
  if (!response.ok) return null;
  return response.json();
}

const CONNECT_HELP = `Not connected to Wuthering AI.

Run the device login:

    node "\${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --login

It prints a URL and a code for the user to approve. Signing up happens on the
same page, and a new account starts with free credit and no card.`;

async function check() {
  const token = readToken();
  if (!token) {
    console.error(CONNECT_HELP);
    process.exit(2);
  }
  const account = await whoami(token);
  if (!account) {
    console.error(
      `The saved token is not valid — it may have been revoked, or it belongs to a
different deployment. Run the login again:

    node "\${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --login`,
    );
    process.exit(2);
  }
  console.log(`Connected to ${ORIGIN} as ${account.email ?? account.accountId}.`);
}

async function login() {
  const start = await fetch(new URL('/api/cli/login/start', ORIGIN), {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ client: 'claude-code-plugin' }),
  });
  if (!start.ok) {
    console.error(`Could not start a login: ${start.status} ${await start.text()}`);
    process.exit(1);
  }
  const { user_code: userCode, device_code: deviceCode, verification_url: url, interval } =
    await start.json();

  console.log(`
Open this page and approve the request:

    ${url}

Your code:  ${userCode}

The code lasts fifteen minutes. Waiting…
`);

  // Poll no faster than the interval the server asked for. `slow_down` means
  // exactly that and is answered by backing off rather than by retrying harder.
  let wait = (interval ?? 5) * 1000;
  const deadline = Date.now() + 15 * 60 * 1000;
  while (Date.now() < deadline) {
    await new Promise((resolve) => setTimeout(resolve, wait));
    const poll = await fetch(new URL('/api/cli/login/poll', ORIGIN), {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ device_code: deviceCode }),
    });
    const body = await poll.json().catch(() => ({ status: 'error' }));
    if (body.status === 'approved') {
      const file = saveToken(body.token);
      const who = body.account?.email ?? body.account?.accountId ?? 'your account';
      console.log(`Connected as ${who}. The token is saved at ${file} and is not printed.`);
      return;
    }
    if (body.status === 'slow_down') {
      wait += 2000;
      continue;
    }
    if (body.status === 'pending') continue;
    console.error(`Login ${body.status ?? 'failed'}. Nothing was saved.`);
    process.exit(1);
  }
  console.error('The code expired before it was approved. Run the login again.');
  process.exit(1);
}

function logout() {
  const file = tokenPath();
  if (existsSync(file)) rmSync(file);
  console.log('Forgotten. The token is still valid until it is revoked at ' + `${ORIGIN}/dashboard.`);
}

// `call.mjs` imports `readToken` from here, so the command line only runs when
// this file is what was executed. Without the guard, importing it ran its own
// argument parser against the caller's arguments.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const mode = process.argv[2] ?? '--check';
  if (mode === '--check') await check();
  else if (mode === '--login') await login();
  else if (mode === '--logout') logout();
  else {
    console.error('Usage: login.mjs [--check | --login | --logout]');
    process.exit(64);
  }
}
