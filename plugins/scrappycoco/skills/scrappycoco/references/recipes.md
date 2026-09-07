# Scrappycoco recipes

Use these only after setup succeeds. Each recipe starts by inspecting the live
contract; if the returned schema differs from the example, follow the schema.
Omitting `--provider` uses the first two available providers in catalog order.
A single `--provider` pins execution to that provider; it has no automatic
fallback. Repeat `--provider` to supply the exact ordered fallback list, with
each provider's tested options. Run advances on provider errors or empty results;
it does not assess whether returned records satisfy the task. Gateway failures
before provider execution cannot trigger this fallback. For local-business work,
test locality and required local-pack fields before selecting a backup.

## Extract one page

```bash
scrappycoco catalog inspect web.extract_content --json
scrappycoco run web.extract_content \
  --input '{"url":"https://example.com"}' \
  --output page.json --format json --json
```

The file contains records. Stdout contains the request ID, usage, provider
evidence, record count, and output path. Judge the requested fields; if the
bounded direct result is incomplete, escalate automatically to Discovery.
For a single URL containing a multi-item directory or search result, compare
captured versus source-reported totals. A result such as `40 of 166` makes the
next paid acquisition step Discover/compare across the default candidates for
all available providers, not another direct same-provider scrolling probe.
Maintain a ledger for every resulting request: distinct request ID, provider
attempt count, billing status, exact provider cost, and exact customer charge.
At handoff, sum finalized exact response usage and state request and attempt
counts separately only when the user requests billing or audit detail; do not
infer either count from agent tool turns. The default handoff should simply
state the completed count, attach the output, mention material gaps, and end
with one specific next-task question such as “Would you like the next batch?”

## Structured output and result reuse

Describe how absent fields should be represented and allow JSON null or omitted
optional fields in the requested extraction schema. Inspect returned values:
providers may emit literal strings such as `"null"` or `"none"`. The calling
agent decides whether a value means missing data from the task, schema, and
source evidence. If needed, normalize a separate local deliverable and disclose
the transformation; preserve the original provider output. Do not blanket-replace
matching strings or infer missing facts.

Save results in the caller's own files or storage when they need to be reused.
Across all providers, job results expire 30 days after completion; inspect `result_expires_at` and
download within that window. An expired result requires a new billable execution
if the caller did not save a copy.
Do not treat idempotency keys or hosted job results as permanent storage.
Use cache/freshness controls only when the live provider-options schema exposes
them; inspect their units and preserve the chosen values in the configuration.
Firecrawl age is milliseconds, Exa age is hours, Scrapfly TTL is seconds, and
SerpApi exposes a cache-bypass boolean. A value of `1` is not portable between
providers. Search publication-date filters do not control cache freshness.
Cache reuse does not guarantee a lower Scrappycoco charge. For Firecrawl search,
page-cache options opt in to scraping results and can add provider usage.

## Extract a batch of pages

Use this direct batch Run for a small bounded batch or when the exact
configuration is already validated for the same page family and output
contract. For an unvalidated batch of 10 or more pages—or a smaller materially
expensive batch—use the representative-page Discovery pattern below.

```bash
scrappycoco catalog inspect web.extract_content --json
scrappycoco run web.extract_content \
  --input '{"urls":["https://example.com/a","https://example.com/b"]}' \
  --concurrency 3 --output pages.jsonl --format jsonl --json
```

Use one batch for up to 500 URLs. Check every item status and retry only failed
items with `run --retry-failed RUN_ID` when a retry is appropriate.

## Discover once, then run a repeated-template batch

Bootstrap the directory only far enough to obtain one valid detail URL and a
displayed total when cheap. Do not block Discovery on complete enumeration.
Compare the representative detail page, choose the strongest complete primary
for the user's priority, preserve a tested different-provider fallback, and
classify requested facts absent from the source as enrichment needs. Then ask
once before complete enumeration and batch execution.

```bash
scrappycoco catalog inspect web.extract_content --json
# First use a bounded Run on the directory to obtain REPRESENTATIVE_DETAIL_URL.
scrappycoco discover --file discovery.json --json
scrappycoco discover --id DISCOVERY_ID \
  --test --input '{"url":"REPRESENTATIVE_DETAIL_URL"}' \
  --output discovery-test.json --json
scrappycoco discover --id DISCOVERY_ID \
  --update discovery-update.json --json
scrappycoco discover --id DISCOVERY_ID --finalize --json
# Ask once here. After yes, enumerate the unique target set and record its count.
scrappycoco run web.extract_content \
  --input '{"urls":["https://example.com/a","https://example.com/b"]}' \
  --provider PRIMARY_PROVIDER --provider FALLBACK_PROVIDER \
  --provider-options '{"PRIMARY_PROVIDER":{"EXACT_PRIMARY_OPTION":true},"FALLBACK_PROVIDER":{"EXACT_FALLBACK_OPTION":true}}' \
  --output pages.jsonl --format jsonl --json
```

Follow the Discovery workbook when authoring `discovery.json` and evaluating
candidate evidence. Treat the target set as a ledger: preserve successes, retry
only unresolved targets with a material change, use the fallback where useful,
and reconcile captured versus expected before claiming completion.

## Search the web

```bash
scrappycoco catalog inspect web.search_web --json
scrappycoco run web.search_web \
  --input '{"query":"electric vehicle battery recycling companies"}' \
  --limit 20 --output search-results.csv --format csv --json
```

## Search X

```bash
scrappycoco catalog inspect x.search_posts --json
scrappycoco run x.search_posts \
  --input '{"query":"AI agents"}' \
  --limit 20 --output x-posts.json --format json --json
```

## Search Reddit

```bash
scrappycoco catalog inspect reddit.search_posts --json
scrappycoco run reddit.search_posts \
  --input '{"query":"AI agents"}' \
  --limit 20 --output reddit-posts.json --format json --json
```

Treat social records as public-discussion evidence, not authoritative company
statements.

## Retrieve company filings

```bash
scrappycoco catalog inspect filings.edgar_filings --json
scrappycoco run filings.edgar_filings \
  --input '{"ticker":"NVDA"}' \
  --limit 20 --output filings.csv --format csv --json
```

## Continue a cursor monitor

Inspect the relevant monitor contract before both the initial and later run:

```bash
scrappycoco catalog inspect reddit.monitor --json
scrappycoco run reddit.monitor \
  --input '{"query":"AI agents"}' \
  --output initial.json --json
```

Save the returned cursor. On the next requested or scheduled check:

```bash
scrappycoco catalog inspect reddit.monitor --json
scrappycoco run reddit.monitor \
  --input '{"query":"AI agents","since":"CURSOR"}' \
  --output updates.json --json
```

## Keep a long run out of the foreground

```bash
scrappycoco catalog inspect web.crawl_site --json
scrappycoco run web.crawl_site \
  --input '{"url":"https://example.com"}' --detach --json
```

The response includes `job_id` and an exact `next_command`. Wait and save later:

```bash
scrappycoco jobs wait JOB_ID \
  --output crawl.jsonl --format jsonl --json
```

## Build a reusable scraper

Use Discover only when provider or configuration choice is uncertain:

```bash
scrappycoco catalog inspect web.extract_content --json
scrappycoco discover --file discovery.json --json
scrappycoco discover --id DISCOVERY_ID \
  --test --input '{"url":"https://example.com/products"}' \
  --output discovery-test.json --json
scrappycoco discover --id DISCOVERY_ID \
  --update discovery-update.json --json
scrappycoco discover --id DISCOVERY_ID --finalize --json
scrappycoco run --config DISCOVERY_ID \
  --input '{"url":"https://example.com/products"}' \
  --output products.json --json
```

Follow the Discovery workbook for the required JSON structures and evaluation
checks.


### Native batches

For any capability, `input.items` accepts up to 500 independent capability inputs.
Web search also accepts `input.queries`; extraction retains `input.urls`. Native
batching is automatic where supported. Inspect catalog `batch_mode` and
`batch_reason`; individual execution is explicitly reported. `limit` applies per
input. Preserve response `batch_items` and indexed attempts. Do not resubmit
native tasks marked pending or submission-unknown before reconciling their IDs.
