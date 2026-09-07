# GEO evidence workbook

Use this workflow for GEO, AEO, AI-visibility, answer-engine citation, or
"what does an AI say about" requests. The goal is to observe named answer
engines directly and preserve their answers and citations. Ordinary web search
is useful supplemental evidence, but it is not a substitute.

## 1. Define comparable inputs

Write the prompt or query set before execution. Record the requested engines,
country, state or location, device, and any time-sensitive wording. Use the same
materially equivalent prompt across engines. If prompt variants are required,
apply the same variants to every engine and keep each variant separate.

Choose the evidence depth before running:

- A **snapshot** may use one or more prompts with one observation per engine,
  but it must be labeled a snapshot and must not claim ranking, frequency, or
  general visibility.
- For a **GEO benchmark or ranking report**, consider using roughly 10 or more
  prompts spanning several intent families (for example branded, category,
  problem/solution, comparison, or buying intent) and two or more independent
  repetitions of each prompt-engine pair. The calling agent chooses the sample
  design that fits the user's goal, confidence needs, time, and cost, and records
  that design before drawing conclusions.

For stronger comparability, prefer freezing the prompt set and variants before
the first billable request. If evidence motivates a later exploratory prompt,
label it post hoc and do not mix it silently into the original benchmark.

## 2. Inspect the direct routes

Inspect both contracts even if `catalog list --available` omitted the desired
provider:

```bash
scrappycoco catalog inspect web.research --json
scrappycoco catalog inspect web.search_web --json
```

Use the live provider IDs, availability reasons, option schemas, and defaults.
`web.research` may expose answer-engine responses; `web.search_web` may expose
search-engine AI overviews. Select each required engine explicitly. Do not let a
generic default route stand in for the user's named engine.

For Google AI Overview, `include.aioverview` is an object such as
`{"markdown":true}`, not a boolean. Inspect `outputs.ai_overview` on the first
record and preserve `outputs.native_response` as the verbatim provider envelope.

## 3. Handle unavailable direct evidence

If a required route is unavailable, report its exact catalog reason and mark
that engine's direct observation blocked. Do not silently replace it with a
SERP provider, a generic research provider, or extracted listicles. These may
be gathered only as a separately labeled supplemental layer.

Maintain enough execution evidence to reconcile every reported claim. A useful
ledger has one row for each requested prompt, variant, repetition, and engine,
including unavailable engines, and commonly tracks:

- requested engine and inspected provider ID;
- prompt ID, variant ID, repetition, locale, and supported device options;
- request ID, job ID, idempotency key, attempted provider, and exact options;
- status: `unavailable`, `not_attempted`, `attempted`, `captured`, `refused`,
  `empty`, or `failed`;
- output file, citations present, truncation, finalized cost, and unresolved
  cost count.

An unavailable or failed engine remains in the ledger. Never infer the result
of an unattempted prompt from another failure by the same engine.

## 4. Run and verify each engine

Use exact inspected provider options and save records to files. For each engine,
verify all of the following before analysis:

- The attempted and returned provider is the intended engine route.
- The answer representation exists in `text` or `outputs` and matches
  `primary_format`.
- Citations or sources and `native_response` are preserved when the provider
  returns them.
- Locale, device, and other material native options match the test contract.
- Errors, empty answers, and truncation markers are recorded.
- `status: ok` is treated only as transport completion, not useful evidence.

For multiple independent answer-engine calls, consider queuing requests with
`--detach` before waiting for results when that materially improves wall time or
responsiveness. The CLI serializes OAuth credential refresh safely, so an agent
may run independent provider work concurrently within known account and
provider limits. Foreground or sequential execution remains valid when it is
simpler or better suited to the task. When using durable jobs, collect each with
`jobs wait` and preserve its job-to-output mapping.

The calling agent decides whether and how to retry from the error evidence,
user goal, cost, and likelihood of a transient failure. Avoid blind unchanged
retry loops; a materially changed input, provider, native option, acquisition
method, or delayed retry may be appropriate. Reuse an idempotency key only when
the original response is unknown and the request is byte-for-byte identical;
otherwise use a new key for the changed billable request. Never claim a key was
reused unless it was explicitly supplied, and never generalize from an engine
whose requested answer was not captured.

Treat a safety refusal as `refused`, not as a missing route or knowledge gap.
When the user's goal benefits from distinguishing a prompt-specific refusal
from a systematic one, consider a materially different neutral paraphrase. For
comparative evidence, applying the same variant to comparable engines usually
produces stronger evidence. One refusal alone does not establish systematic
refusal.

## 5. Analyze reproducibly

Calculate entity mentions, answer positions, citation domains, and frequency
from the saved direct outputs with a reproducible script or query. Do not hand
author counts. Preserve the prompt-to-engine-to-output mapping so every claim
can be traced back to one direct observation.

Normalize citation URLs by parsed hostname. Count the target's own citations
only when the hostname equals the target domain or one of its subdomains; a URL
that merely contains the brand string is not an own-domain citation. Derive
denominators from `captured` ledger rows only, and show refused, empty, failed,
unavailable, and not-attempted counts separately.

When `metadata.citation_evidence_source` is `answer_links_fallback`, the provider
omitted its structured source list and Scrappycoco deterministically recovered
links from the answer text. Preserve that provenance and let the calling agent
decide whether each link counts as a citation for the task.

Keep direct engine evidence separate from:

- Organic or semantic search results.
- Generic research synthesis.
- Extracted competitor pages and listicles.
- The calling agent's own interpretation.

## 6. Handoff

Lead with tested versus requested engines, then report answer and citation
findings. Name blocked or empty engines, locale/device, prompt variants, and any
truncation. Label supplemental SEO or competitor research explicitly and never
describe it as observed answer-engine output.

Reconcile requested, attempted, and captured observations before every handoff,
and report other material states such as refused, failed, unavailable, or
not-attempted when present.
Report finalized cost separately from pending or unresolved cost; never call a
reconciliation-pending attempt free or unbilled. Claim ranking or frequency
only to the extent supported by the declared sample design; otherwise call the
result a snapshot and limit conclusions to the exact captured observations.
