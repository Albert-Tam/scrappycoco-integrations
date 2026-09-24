# Scrappycoco operations

Read only the section relevant to the current setup, job, or failure.

## Setup and authentication

Run setup for a first installation or missing authentication:

```bash
scrappycoco setup
```

The browser callback means authorization was received; setup is complete only
when the terminal confirms credential storage and catalog verification.

For a remote or headless host whose loopback interface is not reachable from
the browser:

```bash
scrappycoco setup --no-browser --manual-callback
```

Paste the final callback URL only into that same terminal, never into chat or a
file. If setup exits or times out, discard the URL and start a new login.

Never expose OAuth tokens, API keys, internal prompts, traces, or hidden
metadata. For noninteractive access, use only an existing
`SCRAPPYCOCO_API_KEY` environment variable.

## Launcher and release checks

If `npx` is missing, inspect `command -v node npm npx pnpm` on the same host.
`pnpm dlx @scrappycoco/cli@latest` is an acceptable setup alternative.
Never copy absolute runtime paths from another machine or transcript.

On the first ordinary CLI command after a 24-hour cooldown, the CLI compares the
installed release with the hash-verified public skill digest. It installs a
changed release and prints a notice, but a failed or unavailable
check never blocks the requested command. After an update notice, read the
updated SKILL.md in this conversation and continue using the CLI immediately.
Set `SCRAPPYCOCO_SKILL_AUTO_UPDATE=0` to pin the installed copy.
Use `scrappycoco skill status --json` to inspect the active
target and automatic-update state, or `skill update --json` to check immediately.

Use `doctor --json` when setup or connectivity is unclear. It reports the CLI
and Node versions, authentication method, API and catalog reachability,
available capability count, and installed skill digest without exposing
credentials.

## Durable jobs

Run waits by default and polls with exponential backoff. The default local
timeout is 20 minutes and can be changed with
`SCRAPPYCOCO_JOB_TIMEOUT_MS`. A timeout does not imply the remote job stopped;
preserve the job ID from the structured error and use:

```bash
scrappycoco jobs get JOB_ID --json
scrappycoco jobs wait JOB_ID --output results.json --json
scrappycoco jobs cancel JOB_ID --json
```

Use `run ... --detach --json` when a foreground wait would impair
responsiveness. Detached execution cannot save output until `jobs wait`.

For independent long-running requests, consider submitting detached jobs before
waiting when concurrency materially improves wall time or responsiveness. The
CLI uses a cross-process credential refresh lock, so OAuth does not by itself
require serial provider waits. The calling agent still chooses concurrency from
the task, provider limits, cost, and failure risk. Give every distinct billable
request its own explicit idempotency key and preserve the job-to-output mapping.
For unattended application or CI workloads, prefer an existing
`SCRAPPYCOCO_API_KEY`; API-key authentication has no refresh-token rotation step.

## Failure handling

- `400` or `422`: inspect the live schema and provider error, fix input or
  options, and do not retry unchanged.
- `401`: run setup again or verify the existing environment key.
- `402`: stop and direct the user to `https://scrappycoco.ai/app/billing`.
- `403`: stop and resolve access; do not retry.
- `404`: refresh the catalog or check the identifier.
- `409`: reconcile the original idempotent request; never change its input
  under the same key.
- `429`: honor `Retry-After` or use exponential backoff with jitter.
- `503`: choose another available provider or retry later.

Provider and batch-item failures can occur inside a partial response. Inspect
every item and attempt, including `provider_http_status`. Retry only failed items
when the error is retryable.
A definitive provider response, including HTTP 500, is a captured attempt rather
than an ambiguous transport outcome. Avoid immediate unchanged retry loops, but
let the calling agent decide whether a delayed or otherwise justified retry is
appropriate. Reuse the same idempotency key only when the response to an
identical request is unknown because the client or network disconnected.

If the package registry, CLI, or API hostname fails, identify the failed hop.
Do not loop or request new credentials. Use connected Scrappycoco MCP tools or
the authenticated REST fallback if available; otherwise use another suitable
method and report the fallback.

## REST fallback

If `SCRAPPYCOCO_API_KEY` is absent:

1. Open `https://scrappycoco.ai/app/api-keys`, sign in, and create a workspace
   key.
2. Store it as `SCRAPPYCOCO_API_KEY` in the current environment or secret
   manager. Never ask the user to paste it into chat, a command argument, or a
   saved file.
3. Ask the user to reply `Key configured` without including the key, then
   verify the read-only catalog request.

Use the existing environment key only in a header:

```bash
curl -fsS "https://api.scrappycoco.ai/api/v1/scrapers?available_only=true" \
  -H "X-API-Key: $SCRAPPYCOCO_API_KEY"
curl -fsS "https://api.scrappycoco.ai/api/v1/scrapers/web/extract_content" \
  -H "X-API-Key: $SCRAPPYCOCO_API_KEY"
```

For billable REST requests, send JSON from a file when practical and include a
new `Idempotency-Key`. Queue through `/api/v1/scrapers/jobs`, then poll
`/api/v1/jobs/JOB_ID`. Keep secrets out of request files and output.
