# CompanyEnrich: company and people intelligence

Inspect the current catalog before constructing a request. CompanyEnrich exposes
native record search, enrichment, workforce, lookalikes, people and email lookup,
reference dictionaries, bulk/export jobs and account lists through the same Run
contract. The calling client judges fit; native similarity scores/ranks remain
provider evidence. They are not a gateway-selected winner.

## Inspect and run a bounded query

```bash
scrappycoco catalog list --source company --json
scrappycoco catalog inspect company.search_records --json
scrappycoco catalog inspect people.search --json
```

Native POST JSON is under `input.body`. Required query/path values are top-level
input fields; optional native query parameters are in the inspected provider
options. Use provider enum values and reference lookups rather than guessing.
A complete company search request file:

```json
{
  "input": {"body": {"query": "Stripe", "pageSize": 1}},
  "providers": ["companyenrich_api"],
  "provider_options": {"companyenrich_api": {}},
  "limit": 1
}
```

```bash
scrappycoco run company.search_records --file request.json --output companies.json --json
```

Save the records and full receipt. Read actual native results and pagination,
not just the CLI exit status. A completed gateway job may contain failed provider
attempts. Inspect `attempts[].status`, `provider_http_status`, `error` and
`native_response`. REST and MCP accept the same input/options; MCP uses the
inspected `scraper_id`. Do not send the provider key to the CLI or a request file;
the gateway manages it.

## Select the right contract

| Need | Capability hints |
| --- | --- |
| Company by domain/properties/ID | `company.enrich_domain`, `company.enrich_properties`, `company.get_record` |
| Company native search | `company.search_records`, `company.search_preview`, `company.search_count`, `company.search_scroll` |
| Lookalikes | `company.find_similar`, `company.similar_preview`, `company.similar_count`, `company.similar_scroll` |
| Headcount/history | `company.workforce` (exactly one of domain or CompanyEnrich UUID) |
| Domain suggestions | `company.autocomplete` |
| People/roles | `people.search`, `people.scroll`, `people.get_record`, `people.education` |
| Reverse work-email lookup | `people.lookup_email` |
| Work-email resolution | `people.email` (native status/certainty; beta) |
| Filter dictionaries | `reference.regions`, `reference.country`, `reference.countries`, `reference.states`, `reference.cities`, `reference.industries`, `reference.keywords`, `reference.technologies`, `reference.positions` |
| Explicit synchronous domain batch | `company.enrich_batch` (up to 50 domains) |

CompanyEnrich company IDs are UUIDs; person IDs are integers. They are not
Coresignal IDs. Coresignal `company.search`/`employee.search` return dataset IDs;
CompanyEnrich `company.search_records`/`people.search` return records. Preserve
provider and options in saved configurations rather than translating IDs or filters.

`pageSize` controls native paged results. If omitted where supported, the gateway
uses `min(limit, 100)`; explicit native values prevail. Complete returned pages are
retained. Follow `nextCursor` through `body.cursor`, or page metadata through
`body.page`, only within the mandate. Page search has a 10,000-result ceiling;
scroll is a separate capability. Counts and previews are not full records.
Previews may require a different plan; inspect failures instead of inferring that
all search is unavailable. An enrichment queued by `waitForEnrichment=false`
may be incomplete; preserve its status rather than declaring an enriched profile.

Optional `expand` can incur additional credits: workforce is five per company,
education one per person. Only request fields needed for the task. Email resolution
charges depend on newly accessed found emails; success alone does not prove a new
charge. Preserve native `status` and `certainty`; do not label every returned email
verified or guess an address when none is found.

## Native batches and account resources

`company.enrich_domain` with `input.items` uses native batches of 50 and correlates
by domain, preserving duplicate caller entries and missing/ambiguous failures.
`waitForEnrichment=false` uses individual calls because the native batch contract
cannot preserve that option. `people.email` with `input.items` uses native async
bulk resolution; submissions and job IDs are checkpointed, charged once per batch,
and resumed by ID. Unknown submissions are not silently resubmitted. Inspect
batch receipts before retrying. Pending upstream work is not a completed lookup.

The `provider.*` capabilities expose CompanyEnrich's shared account controls to
the authenticated gateway owner only. These include bulk/export creation and
status, job/list enumeration, list create/get/update/delete and account information.
Native `lists` filters also require owner access. A customer cannot access another
customer's upstream jobs or lists by supplying an ID. Owners should use explicitly
scoped disposable lists for tests and resume existing jobs rather than recreate them.
Results URLs remain native evidence; do not attach provider credentials when
retrieving a presigned file. These controls do not create a Scrappycoco scheduler.

## Cost and evidence

Use the live pricing description and actual usage evidence. USD is unresolved
unless the account's credit rate is configured; do not infer a rate from a free
credit balance or treat unresolved as zero. Async job creation remains unresolved
until its completion charge is reconciled; status reads are free and preserve the
reported original job charge without charging it again. Provider errors retain
native evidence and unknown costs conservatively.

For sales, verify role/company identity and observation date before outreach.
For marketing, assess audience fit and claims before creative adaptation. Public
records do not establish purchase intent, contact consent or campaign effectiveness.

Official reference: [CompanyEnrich API index](https://docs.companyenrich.com/llms.txt).
