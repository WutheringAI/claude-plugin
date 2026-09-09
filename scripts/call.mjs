#!/usr/bin/env node
/**
 * Make one Wuthering AI call, without the token passing through the transcript.
 *
 *   node call.mjs --list
 *   node call.mjs web_search query="ai agent pricing"
 *   node call.mjs keyword_ideas keywords="ai agent,ai agents" limit=50
 *
 * Arguments are `key=value`. A value containing commas is an array, which is
 * what the API expects on a query string.
 *
 * The credential is read from disk by this process and put in a header. It is
 * never an argument, never printed, and never in the URL — an agent that pastes
 * a token into a shell command has written it into a transcript that will be
 * stored and probably summarised somewhere else.
 */
import { readToken } from './login.mjs';

const ORIGIN = process.env['WUTHERING_ORIGIN'] ?? 'https://wutheringai.com';

const argv = process.argv.slice(2);
if (argv.length === 0) {
  console.error('Usage: call.mjs <tool> key=value …   |   call.mjs --list');
  process.exit(64);
}

/** The tool list is free and needs no credential, so it is fetched first. */
if (argv[0] === '--list') {
  const response = await fetch(new URL('/v1', ORIGIN));
  const index = await response.json();
  const tools = index.tools ?? [];
  console.log(`${tools.length} tools at ${ORIGIN}/v1\n`);
  for (const tool of tools) {
    const slug = tool.slug ?? String(tool.path ?? '').split('/').pop();
    console.log(`${slug}\n  ${tool.summary ?? ''}`);
    for (const param of tool.params ?? []) {
      const required = param.required ? ' (required)' : '';
      console.log(`    ${param.name}: ${param.type}${required}`);
    }
    console.log('');
  }
  process.exit(0);
}

const [slug, ...rest] = argv;
const token = readToken();
if (!token) {
  console.error(
    `Not connected. Run:\n\n    node "\${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --login\n`,
  );
  process.exit(2);
}

const url = new URL(`/v1/${slug}`, ORIGIN);
for (const pair of rest) {
  const at = pair.indexOf('=');
  if (at === -1) {
    console.error(`Arguments are key=value. "${pair}" is neither.`);
    process.exit(64);
  }
  url.searchParams.set(pair.slice(0, at), pair.slice(at + 1));
}

const response = await fetch(url, { headers: { authorization: `Bearer ${token}` } });
const text = await response.text();

if (response.ok) {
  // Pretty-printed: this output is read by a model and by a person over its
  // shoulder, and a wall of minified JSON serves neither.
  try {
    console.log(JSON.stringify(JSON.parse(text), null, 2));
  } catch {
    console.log(text);
  }
  process.exit(0);
}

let message = text.slice(0, 400);
try {
  message = JSON.parse(text).error?.message ?? message;
} catch {
  /* the body was not JSON; the raw text is the best available message */
}

// Each of these has one correct response, and none of them is "try again".
const ADVICE = {
  401: `The token was refused. Run: node "\${CLAUDE_PLUGIN_ROOT}/scripts/login.mjs" --login`,
  402: `Out of credit. The user tops up at ${ORIGIN}/dashboard. Do not retry.`,
  404: `No tool called "${slug}". Run: node "\${CLAUDE_PLUGIN_ROOT}/scripts/call.mjs" --list`,
  429: `Rate limited${response.headers.get('retry-after') ? ` — wait ${response.headers.get('retry-after')}s` : ''}. This is not an error to work around.`,
  502: 'The source failed. This call was not charged. One retry is reasonable; a loop is not.',
  503: 'Billing is unavailable, so nothing was called and nothing was charged. Try again shortly.',
};

console.error(`${response.status}: ${message}`);
if (ADVICE[response.status]) console.error(ADVICE[response.status]);
process.exit(1);
