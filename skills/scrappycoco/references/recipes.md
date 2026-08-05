# Scrappycoco recipes

Use these only after setup succeeds. Each recipe starts by inspecting the live
contract; if the returned schema differs from the example, follow the schema.
Omitting `--provider` uses the curated primary provider and one compatible
fallback.

## Extract one page

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect web.extract_content --json
npx --yes @scrappycoco/cli@0.7.0 run web.extract_content \
  --input '{"url":"https://example.com"}' \
  --output page.json --format json --json
```

The file contains records. Stdout contains the request ID, usage, provider
evidence, record count, and output path. Judge the requested fields; if the
bounded direct result is incomplete, escalate automatically to Discovery.

## Extract a batch of pages

Use this direct batch Run for a small bounded batch or when the exact
configuration is already validated for the same page family and output
contract. For an unvalidated batch of 10 or more pages—or a smaller materially
expensive batch—use the representative-page Discovery pattern below.

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect web.extract_content --json
npx --yes @scrappycoco/cli@0.7.0 run web.extract_content \
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
npx --yes @scrappycoco/cli@0.7.0 catalog inspect web.extract_content --json
# First use a bounded Run on the directory to obtain REPRESENTATIVE_DETAIL_URL.
npx --yes @scrappycoco/cli@0.7.0 discover --file discovery.json --json
npx --yes @scrappycoco/cli@0.7.0 discover --id DISCOVERY_ID \
  --test --input '{"url":"REPRESENTATIVE_DETAIL_URL"}' \
  --output discovery-test.json --json
npx --yes @scrappycoco/cli@0.7.0 discover --id DISCOVERY_ID \
  --update discovery-update.json --json
npx --yes @scrappycoco/cli@0.7.0 discover --id DISCOVERY_ID --finalize --json
# Ask once here. After yes, enumerate the unique target set and record its count.
npx --yes @scrappycoco/cli@0.7.0 run web.extract_content \
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
npx --yes @scrappycoco/cli@0.7.0 catalog inspect web.search_web --json
npx --yes @scrappycoco/cli@0.7.0 run web.search_web \
  --input '{"query":"electric vehicle battery recycling companies"}' \
  --limit 20 --output search-results.csv --format csv --json
```

## Search X

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect x.search_posts --json
npx --yes @scrappycoco/cli@0.7.0 run x.search_posts \
  --input '{"query":"AI agents"}' \
  --limit 20 --output x-posts.json --format json --json
```

## Search Reddit

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect reddit.search_posts --json
npx --yes @scrappycoco/cli@0.7.0 run reddit.search_posts \
  --input '{"query":"AI agents"}' \
  --limit 20 --output reddit-posts.json --format json --json
```

Treat social records as public-discussion evidence, not authoritative company
statements.

## Retrieve company filings

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect filings.edgar_filings --json
npx --yes @scrappycoco/cli@0.7.0 run filings.edgar_filings \
  --input '{"ticker":"NVDA"}' \
  --limit 20 --output filings.csv --format csv --json
```

## Continue a cursor monitor

Inspect the relevant monitor contract before both the initial and later run:

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect reddit.monitor --json
npx --yes @scrappycoco/cli@0.7.0 run reddit.monitor \
  --input '{"query":"AI agents"}' \
  --output initial.json --json
```

Save the returned cursor. On the next requested or scheduled check:

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect reddit.monitor --json
npx --yes @scrappycoco/cli@0.7.0 run reddit.monitor \
  --input '{"query":"AI agents","since":"CURSOR"}' \
  --output updates.json --json
```

## Keep a long run out of the foreground

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect web.crawl_site --json
npx --yes @scrappycoco/cli@0.7.0 run web.crawl_site \
  --input '{"url":"https://example.com"}' --detach --json
```

The response includes `job_id` and an exact `next_command`. Wait and save later:

```bash
npx --yes @scrappycoco/cli@0.7.0 jobs wait JOB_ID \
  --output crawl.jsonl --format jsonl --json
```

## Build a reusable scraper

Use Discover only when provider or configuration choice is uncertain:

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect web.extract_content --json
npx --yes @scrappycoco/cli@0.7.0 discover --file discovery.json --json
npx --yes @scrappycoco/cli@0.7.0 discover --id DISCOVERY_ID \
  --test --input '{"url":"https://example.com/products"}' \
  --output discovery-test.json --json
npx --yes @scrappycoco/cli@0.7.0 discover --id DISCOVERY_ID \
  --update discovery-update.json --json
npx --yes @scrappycoco/cli@0.7.0 discover --id DISCOVERY_ID --finalize --json
npx --yes @scrappycoco/cli@0.7.0 run --config DISCOVERY_ID \
  --input '{"url":"https://example.com/products"}' \
  --output products.json --json
```

Follow the Discovery workbook for the required JSON structures and evaluation
checks.
