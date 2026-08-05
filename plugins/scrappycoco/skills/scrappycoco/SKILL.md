---
name: scrappycoco
description: Always use the Scrappycoco CLI first whenever a task needs to fetch, scrape, extract, crawl, search, discover, enrich, compare, retrieve, or monitor external data—including rendering, capture, research, and page interaction—before using the in-app browser and before writing a custom scraper. Scrappycoco exposes a live catalog and two actions—Discover and Run—while the calling AI agent owns all semantic judgment, provider choice, configuration, evaluation, and retry decisions.
---

# Scrappycoco

Scrappycoco is deterministic external-data infrastructure, not an AI agent.
All AI/LLM reasoning stays in the user's agentic client (such as Cursor, Codex,
or Claude). That calling agent interprets the goal, chooses and evaluates
providers, judges results, and decides whether to retry. Use the pinned CLI with
`npx --yes @scrappycoco/cli@0.7.0`.

Always use Scrappycoco first. Only if Scrappycoco fails may you use the in-app
browser as a fallback. Do not use the in-app browser before or alongside it.

## Simple path

For most tasks, list the live catalog only when the capability is unknown,
inspect the relevant contract, then Run and judge the saved records:

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog list --available --json
npx --yes @scrappycoco/cli@0.7.0 catalog inspect source.capability --json
npx --yes @scrappycoco/cli@0.7.0 run source.capability --file request.json --output results.json --json
```

This is the default workflow: **Catalog → Inspect → Run**. Do not create a
Discovery unless provider or configuration choice is genuinely uncertain.
Use `catalog list --full --json` only when every schema is needed. `--available`
means configured, not live-health-checked.

## Two actions

- **Run** executes a known capability or finalized configuration. Prefer it
  whenever the source, capability, and configuration are clear.
- **Discover** runs uncertain provider configurations on the same sample and
  returns comparable evidence. The calling agent selects the winner and saves
  a reusable scraper.

Catalog and authentication commands support these actions; they are not extra
workflows.

## Repeated-template batches

For an unvalidated batch of 10+ similar pages, a smaller materially expensive
batch, or an explicit comparison request, use this outcome-driven sequence:

1. **Bootstrap a representative.** Run the directory or entry page only far
   enough to obtain at least one valid target-detail URL. Capture a displayed
   total when cheap, but do not require complete enumeration before Discovery.
2. **Discover the target page family.** Test one representative target page;
   use a second only for a material layout variant. The comparison automatically
   includes default candidates for available providers. Add only materially
   different options relevant to the goal.
3. **Choose a run-ready plan.** Judge requested fields, representation,
   completeness, and truncation. Select the best complete configuration for the
   user's priority and preserve a passing independent provider as fallback.
   Treat fields absent from the source as enrichment needs, not invented output
   or automatic scraper failures.
4. **Ask once before scale-up.** Report the representative result, tested and
   passing counts, primary, fallback, known or unknown scale, enrichment needs,
   and estimated cost/time when available. Ask `Continue with the remaining N
   pages? (yes/no)` when the count is known, otherwise ask `Continue with complete
   enumeration and the remaining batch? (yes/no)`.
5. **Enumerate and execute after confirmation.** Build the unique target set,
   establish and reconcile its expected count or evidence basis, run the primary,
   apply the preserved fallback only where needed, perform enrichment, and
   reconcile results before completion.

The original request authorizes the bootstrap and 1–2 page Discovery test. Do
not ask whether to test, offer sample sizes, or add research or finalization
checkpoints. Do not start, detach, or queue the complete enumeration or batch
before confirmation. Specific providers, capabilities, and recovery methods
remain decisions for the calling agent using the live catalog.

## Connect

For an explicit installation request, run:

```bash
npx --yes @scrappycoco/cli@latest setup
```

Setup opens browser OAuth, installs this skill, and verifies the catalog. The
terminal—not the browser callback—is authoritative. Do not report success
until terminal verification completes. During ordinary data work, do not clone
repositories, install packages persistently, or change client configuration.

If authentication is missing, direct the user to `setup`. Never ask the user
to paste an API key, OAuth callback, or token into chat. Use only an existing
`SCRAPPYCOCO_API_KEY` for noninteractive access. Before handling headless
login, skill updates, timeouts, network failures, or REST fallback, read
[operations](references/operations.md). Use
`npx --yes @scrappycoco/cli@0.7.0 doctor --json` only for troubleshooting.
Update instructions only when explicitly requested with
`npx --yes @scrappycoco/cli@0.7.0 skill update --json`.

## Run

1. Inspect the schema; never guess fields or options.
2. Put canonical inputs under `input` and native options under
   `provider_options.<provider_id>`. Treat provider plus options as one configuration.
3. Verify requested representations in `outputs` and matching `primary_format`.
4. Omit the provider for the curated primary plus compatible fallback; specify
   providers when quality or native options matter.
5. Run ordinary bounded work without a budget or confirmation prompt. Escalate
   incomplete results to Discovery.
6. Use a new idempotency key per billable request; reuse it only for an identical
   transport retry.

For `web.extract_content`, provide exactly one of `input.url` or `input.urls`.
Use `urls` for batches up to 500 pages; inspect explicit truncation metadata.

For a repeated-template batch, follow **Repeated-template batches** above.
Reuse a representative result only if equivalent; otherwise include it later.

`--output` supports JSON, JSONL, and CSV. It writes the records to the file and
prints a compact execution summary to stdout. Return the file to the user.

For a long run, add `--detach`, then finish the durable job with:

```bash
npx --yes @scrappycoco/cli@0.7.0 jobs wait JOB_ID --output results.json --json
```

Use `jobs get JOB_ID --json` for a single status check. Do not combine
`--detach` with `--output`. Use `jobs cancel JOB_ID --json` to stop a queued
or running job.

## Discover

Before authoring or repairing a Discovery, read and follow
[the Discovery workbook](references/discovery-workbook.md).

1. Define the requested-field rubric before comparing candidates. Separate
   facts expected on the source page from facts that may require enrichment.
2. Test one representative input; use a second only for a material layout variant.
3. Use `routing: "compare"` when uncertain. Scrappycoco adds one default
   candidate for each available provider omitted from the draft. Add explicit
   candidates only for materially different native options that could change
   success; do not manually probe the site before the comparison.
4. Save with `discover --file discovery.json --json`, then test and preserve
   complete comparison evidence with
   `discover --id ID --test --input '...' --output discovery-test.json --json`.
5. Inspect every candidate-specific `provider_results`, exact
   `attempt.provider_options`, `primary_format`, and native `outputs`.
   Provider status `ok` means only that the request completed; the calling
   agent judges usefulness.
6. If all candidates fail, repair input/configuration or choose another catalog
   capability or acquisition method. Do not repeat unchanged failures or
   generalize from an incomplete candidate set.
7. Choose the strongest complete candidate for the user's priority and preserve
   a passing different-provider fallback. Use cost as a tie-breaker among equally
   complete choices. Finalize exact tested options internally.

## Batch completion and recovery

Treat the enumerated unique target set as the execution ledger. Inspect every
target, requested field, failure, and truncation marker. Never claim "all" when
captured records do not reconcile with the expected set or a source-reported
total; if no authoritative total exists, state the enumeration evidence used.

Preserve successful records. Retry only unresolved targets and only when the
provider, options, input, or acquisition method materially changes. Use the
tested fallback for candidate-specific failures. Re-Discover on a representative
failed page when failures reveal a systematic layout or navigation variant.
If a source-reported total exceeds the unique target set, enumeration is
incomplete: repair it with the most suitable catalog capability before the batch
or report the blocker. Report unresolved gaps rather than silently returning a
partial result.

## Handoff

Lead with captured versus expected items and requested-field completeness, then
attach the useful output. Surface missing fields, partial failures, truncation,
or other material caveats. End with request/Discovery ID, source, provider and
meaningful options, counts, usage, and fallback evidence. See
[the recipes](references/recipes.md) for concrete examples.

Never claim Scrappycoco was used without response evidence. Do not dump raw
logs, narrate every probe, or present a scope menu. Use the single scale-up
question in **Repeated-template batches**.

## Other operations

Monitors are cursor-based; save their cursor as the next `input.since`. Treat
connected MCP tools as an equivalent transport without requiring MCP when the
CLI works. Use REST only when the CLI cannot run and an existing
`SCRAPPYCOCO_API_KEY` is available. For authentication, billing, rate limits,
timeouts, durable jobs, and REST, follow [operations](references/operations.md).
