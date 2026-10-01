# Research capabilities for sales

Use the execution guide resolved by the role's starting workflow for connection,
Run, Discover, receipts and recovery. This guide maps sales deliverables to
sources and explains what the resulting evidence can establish. The current
environment's live catalog and inspected schemas are authoritative; the IDs
below are lookup hints, not proof of availability. MCP uses equivalent operations.

## Inspect the right source before choosing a workaround

The compact CLI catalog is a JSON array of capabilities. Save complete JSON or
use `catalog list --source SOURCE --json` to narrow it; do not truncate JSON
with `head` or treat the first screenful as the complete tool inventory.
Inspect input schemas and provider options in full before constructing requests.

| Sales need | Capability hints to inspect |
| --- | --- |
| Find matching companies | `company.search_records`, `company.find_similar`, `company.search`, `company.preview` |
| Verify/enrich a known company | `company.enrich_domain`, `company.workforce`, `company.collect`, `company.enrich` |
| Find decision-makers at matching companies | `people.search`, `people.get_record`, `employee.search`, `employee.preview`, `employee.collect` |
| Recheck a known person's current profile | `employee.realtime` |
| Find hiring signals or role requirements | `jobs.search`, `jobs.preview`, `jobs.collect` |
| Find relevant Reddit discussions | `reddit.search_posts`, `reddit.subreddit_feed` |
| Read a Reddit discussion and replies | `reddit.post_comments` |
| Verify websites, other sources or community rules | Relevant live web search/extraction capabilities |

For B2B work, inspect the relevant company/buyer contracts before defaulting to
web directories. For Reddit, inspect native search/feed/comments before generic
web extraction. Query mechanics and billing evidence belong in the execution
guide's database reference; sales fit, recency and outreach claims are evaluated
here in the calling client. Use only capabilities needed for the deliverable.

For example, a B2B pipeline task should inspect company search, buyer lookup
and, when hiring is a useful signal, jobs. Explain the proposed approach in
business terms: "I'll find companies that fit, identify the buyers, and check
relevant hiring signals." Execute a bounded first pass when authorized and
available; mentioning a database in a plan is not using it.

`--available` hides capabilities whose providers are unconfigured. If a relevant
family is absent, use an unfiltered source listing or inspect its known ID:

```bash
scrappycoco catalog list --source reddit --json
scrappycoco catalog inspect reddit.search_posts --json
scrappycoco catalog list --source company --json
scrappycoco catalog inspect company.search --json
```

Read each provider's `available` and `reason`, and distinguish missing credentials,
disabled providers, request failures and no matching records. Configured is not
health-checked. Report a material limitation precisely, e.g. "The company database
isn't configured in this test environment; I'll use public sources for this pass."
Do not ask customers to configure a provider account that the gateway manages.
In an isolated preview, report the missing configuration to the tester; never
switch to production or copy its credentials. Continue independent preparation.

## CompanyEnrich records and contact enrichment

Read the execution guide's CompanyEnrich reference when selecting these routes.
`company.search_records` and `people.search` return native records, while existing
Coresignal search returns IDs. Keep their identifier namespaces and filters
separate. Inspect native query schemas and reference dictionaries before searching.
`company.find_similar` returns provider-ranked lookalikes for the client to assess;
its rank is not a gateway recommendation. `people.lookup_email` resolves a work
email; `people.email` may find an address and returns native status/certainty.
Preserve that evidence rather than promising a verified deliverable mailbox.
Owner-only provider jobs/lists are not customer research shortcuts. A denied
preview is a plan limitation, not proof that paid search is unavailable.

## B2B databases: company → buyer → relevant signal

Inspect the capabilities needed for the requested fields. Current Coresignal
search returns numeric record IDs, preview returns partial records, and collect
returns native records. IDs and query fields depend on dataset. Do not turn a
search-ID list into a company shortlist or label a preview as fully enriched.

Choose the dataset and query type explicitly from the inspected options. Read
provider schema links/data dictionaries for native fields; do not guess filters
or reuse one dataset's fields on another. Search/preview support different query
types. If provider documentation is inaccessible, report that constraint rather
than repeatedly issuing invalid or broad billable queries.

Use a focused ICP query, inspect representative results, then collect the chosen
records with the same dataset and stable IDs. Use `input.items` for supported
native bulk collection, subject to the operational batch/spend boundary. Keep
the search query, dataset, cursor/page and provider/native evidence with results.
Pagination is caller-controlled: follow the returned search cursor or preview
page metadata within scope and report unvisited pages or ceilings. `limit` is
not a guarantee that every provider page is capped at that number.

Join employee evidence to verified company identity, then check current employer,
role and observation date. Use jobs only when the dated role requirements inform
the offer; a vacancy alone is not purchase intent. Verify stale/ambiguous details
with known profiles or company sites. Enrich only fields needed for the next
action. None of these contracts guarantees verified emails: preserve verification
state and reachable routes without guessing addresses. Judge task fit in the
calling client and record gaps before preparing recipient-specific drafts.

## Preserve receipts and qualify claims before drafting

Read the operational skill's database query guide. Save the complete response
receipt for every Run, even empty results and failed attempts, and link receipts
from `activity.md`. Keep request IDs, job IDs, exact finalized customer charges,
attempt counts and unresolved usage. Retrieve an existing job to inspect missing
details instead of issuing another paid Run. Use the inspected pricing to choose
bounded query validation before paid previews. Do not estimate final billing
from tool turns or discard costs through shell output filtering.

Before calling a prospect ready, carry these checks into both the deliverable
and its final summary:

- Job status and dates: `application_active=0` or `deleted=1` means historical
  recruitment, not an open role. Missing status is unknown. Collect status when
  preview omits it; recent `created` dates alone cannot establish current hiring.
- Repeated postings: deduplicate by identity/location before calling them
  reposts; repetition alone does not prove difficulty filling a role.
- Buyer identity: match the employer and role, preserve headline/history
  disagreements, and do not claim current employment from a missing end date alone.
- Buying intent: distinguish observations from hypotheses. Hiring or robotics
  spend does not establish available AI-services budget or manual back-office
  processes. Use conditional outreach wording until those facts are verified.

A failed source does not disable the rest of the catalog. For an agreed broad
research approach, inspect a suitable alternative and continue without asking to
restart the work. Preserve an explicitly required source as an unresolved gap.
An unavailable real-time lookup is a separate capability limitation; search,
preview and collection may still work. Empty query results are not disabled
employee search, and preview output keys are not necessarily searchable fields.

## Reddit: native acquisition and current evidence

When configured, use `reddit.search_posts` for the topic and
`reddit.subreddit_feed` for selected communities. Inspect supported sort/time
filters and pagination, and use a recent window appropriate to the goal. If no
recent matches appear, adjust the query or widen the window visibly within the
mandate. Do not call old relevance current intent.

Read promising discussions through `reddit.post_comments` using its inspected
post-reference input. Preserve post/comment dates, latest relevant activity,
URLs and native pagination/coverage metadata. A returned page is not necessarily
the full comment tree. A web login wall or empty generic extraction does not
show that the Reddit capability failed; inspect/use the dedicated route before
declaring discussion content inaccessible.

Promotion rules are a separate source. Check accessible official community
rules through suitable web tools; the current Reddit contracts do not promise a
rules endpoint. If rules remain inaccessible, mark that specific review gap and
keep the draft unready for posting. Do not infer rules from successful comment
retrieval, treat unknown rules as permission, or move an old thread to a DM.

Generic web search can supplement discovery or provide a fallback when native
capabilities are unavailable or unsuitable. Record the reason for that choice.
Search snippets are leads to investigate, not verified discussions or buyers.
