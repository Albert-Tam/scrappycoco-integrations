# Database queries and evidence

Inspect company, employee and jobs capabilities relevant to the task. Availability
is per capability: disabled `employee.realtime` does not disable database search,
preview or collection. Read each provider's reason separately. Real-time access
requires a provider entitlement and gateway configuration; do not toggle it or
ask the customer to buy access merely to complete ordinary employee research.

## Query before paying for records

Read `input_schema.properties.query`: its native guide links the search mapping
and gives examples scoped to dataset and query type. Read the matching provider
mapping before adding fields. Returned record keys are not a search schema.

For the current Coresignal integration, ID search is metered at zero credits;
preview charges per successful page even when no records match. Inspect current
pricing and retain each response's usage. Where useful, validate the exact native
query with search before previewing or collecting selected IDs in the same
dataset. IDs establish matches, not relevance or complete profiles. Do not run
paid probes to guess fields, or retry unchanged empty queries to inspect errors.
A zero count can mean no matching data, incorrect fields or overly narrow
predicates; it does not prove a field is unsearchable.

Base Elasticsearch examples are in the live catalog. Provider references:

- [Company search mapping](https://docs.coresignal.com/company-api/base-company-api/endpoints/elasticsearch-dsl):
  `headquarters_country_parsed`, `size`, `employees_count`, `industry`.
- [Employee search mapping](https://docs.coresignal.com/employee-api/base-employee-api/endpoints/elasticsearch-dsl):
  `full_name`, `headline`, `country`; nested `experience.company_name`,
  `experience.company_id` and `experience.title`. Keep employer and role conditions
  in one nested query. Preview's flat `company_name` is not that nested path.
- [Jobs search mapping](https://docs.coresignal.com/jobs-api/base-jobs-api/endpoints/elasticsearch-dsl):
  `created` requires `yyyy-MM-dd HH:mm:ss`. For an active-only query, explicitly
  request `application_active: 1` and `deleted: 0`; missing flags are unknown.

These are base-dataset examples, not mappings for clean, multi-source, filters
or semantic search. Resolve those through the catalog's provider links.

## Preserve evidence and costs

Use a unique output basename for each research step. Keep the request JSON,
records and `output.receipt_path` together. The full receipt preserves exact
options, attempts, native responses, batch items, pagination and usage. Inspect
it locally. If missing, retrieve the existing job with `jobs get JOB_ID --json`
or `jobs wait JOB_ID --output records.json --json`; neither submits a new Run.
If a file write fails after completion, recover that job, not a new execution.
Keep stdout JSON separate from stderr; do not parse `2>&1` as JSON or truncate
JSON with `head` before saving it.

Maintain one task ledger keyed by distinct `request_id`, including receipt path,
job ID, capability, attempt count, billing status, exact customer charge and
unresolved count. A batch may have many provider attempts in one request.
Deduplicate retrieved receipts by request ID. Sum finalized
`usage.payg_charge_usd_exact` using decimal arithmetic; do not add the breakdown
or provider cost again. Missing receipts or unresolved usage mean the total is
incomplete, not zero. Never present a call-count estimate as an exact total.

## Judge claims in the calling client

Collect only records needed to support the deliverable and verify identity,
status and observation dates. Preserve native contradictions and unknowns.
`application_active=0` or `deleted=1` is not current hiring evidence; describe
it as historical recruitment. A recent creation date does not override status.
Repeated similar listings may be duplicates or multiple locations, not repeated
failed hiring. A headline alone does not establish a current buyer role when
experience records disagree. A hiring signal or robotics investment does not
prove software budget, manual office work or purchase intent. Label those as
hypotheses and phrase outreach accordingly. Keep these qualifications in the
final summary and drafts, not just the working notes.
