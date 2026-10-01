# Scrappycoco operations

Read only the section relevant to the current setup, job, or failure.

## Setup and authentication

When the user invokes Coco or requests work through it, missing authentication
triggers setup automatically. Do not stop at “run setup,” ask for permission to
start login, or substitute another research tool before offering this connection
flow. Announce that you are connecting Coco and that the user needs to complete
browser sign-in, then run setup using the working invocation:


```bash
scrappycoco setup
```

If only npm is available, use the pinned npm invocation in the execution guide
with `setup`; no global install is required. Setup may install/update the Coco
skill and store login credentials as part of connecting Coco. Preserve the current
host/profile and endpoint. For MCP-only clients, initiate the host's supported
OAuth connection flow instead of installing a CLI.

Keep setup running in a persistent terminal session while the user completes
sign-in and consent. If the browser cannot open, show the authorization URL
emitted by the running process. Do not complete account creation or consent on the
user's behalf. Never ask them to paste passwords, tokens or callback URLs in chat.
The browser callback means authorization was received; setup is complete only
when the terminal confirms credential storage and catalog verification. Read any
updated skill and resume the original request with the same working invocation,
without a new intake or start prompt. No paid research is needed to verify access.

If the user cancels or declines login, stop that flow and offer an explicitly
limited offline alternative. If the host blocks execution or cannot initiate
OAuth, name the exact required user action; do not claim an API outage or retry
unchanged failures. Explicit offline/supplied-file-only work does not need setup.

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

## Connection diagnosis before fallback

A copied skill is instructions, not an authenticated research connection. Before
saying Coco research is unavailable, perform a bounded diagnosis on this host:

1. Check the installed command and the documented managed launcher. If neither
   exists, check the available Node/npm/npx runtime and use the supported pinned
   npm invocation from the execution guide for `doctor --json`. This is an
   ephemeral CLI invocation, not permission to install globally or change config.
2. Check exposed or discoverable Scrappycoco MCP tools using the client's tool
   discovery when available. For an MCP-only client, use that connection directly;
   do not require a CLI installation. A missing CLI says nothing about MCP access.
3. With a working CLI, inspect `doctor --json`. Missing authentication means setup
   must be initiated using the flow above in this host/profile; it does not mean the API is down. The doctor
   skips the catalog request when authentication is missing. Do not print secrets
   or ask for keys in chat. With MCP, use its read-only catalog operation.
4. If authenticated, list and inspect only the relevant live capabilities. Keep
   command-not-found, missing auth, network denial, API failure and individual
   provider unavailability distinct. Use REST only under the existing fallback
   rules and an existing environment key. Stop unchanged retries.

Report the exact observed blocker and what was not tested in one short sentence.
If npm execution is blocked by the host, say that; do not report a service outage.
Keep the proposed creator/hook/trend research visible while login is pending;
resume it after verified setup. If setup remains blocked, label those steps conditional. Do not silently switch to web search or a large brief.
Use external fallbacks only after the applicable Scrappycoco checks fail, clearly
identify the fallback, and preserve the selected research objective and scope.

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

## Saved responses and billing

With `--output`, Run and jobs wait save the full execution response beside the
records as `OUTPUT.REQUEST_ID.receipt.json`; read `output.receipt_path` from the
summary. Keep receipts for empty results and failed attempts too. Retrieve an
existing job if a receipt is missing; never rerun a billable request merely to
read its native error, options or usage. For older CLIs, save stdout from the
original execution separately from stderr. See [the database guide](database-research.md#preserve-evidence-and-costs)
for task-ledger reconciliation. Failed jobs also expose `usage`, an `error_code`
and `retryable` when known, and may include a saved `result`. Read these fields
before deciding what to do; failure does not establish zero charge or zero data.
Do not substitute provider cost for customer charge or infer a debit from a rounded
balance alone. Preserve unknown/unsettled amounts as unknown.

## Failure handling

Classify the failed stage before retrying. For `storage_error` or
`result_persistence_failed`, retrieve the existing job and preserve any saved
result/usage. Do not rerun the provider, change the idempotency key, or shrink the
batch merely to reproduce a deterministic server fault. Report the job ID and
continue suitable independent research within the agreed scope. Never switch a
preview to production. Unclassified server errors require inspecting evidence;
a blanket “submit again” suggestion is not a reason to incur another charge.

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
