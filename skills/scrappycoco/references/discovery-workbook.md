# Discovery workbook

Use this workbook when provider choice or provider-native options are uncertain.
Keep all semantic decisions in the calling agent. Replace example values only
after inspecting the live catalog.

## Contents

- [Decide between Run and Discover](#1-decide-between-run-and-discover)
- [Fill in a complete Discovery](#2-fill-in-a-complete-discovery)
- [Save and test](#3-save-and-test)
- [Select, update, and finalize](#4-select-update-and-finalize)
- [Report an auditable handoff](#5-report-an-auditable-handoff)

## 1. Decide between Run and Discover

Use direct Run for a single page, a small bounded one-off, or an exact
configuration already validated for the same page family and output contract.
Judge the returned records against the requested fields. If the direct result
is incomplete, escalate to Discover automatically instead of asking permission
or manually diagnosing the website. For example, with a known public endpoint:

```json
{
  "input": {
    "url": "https://example.com/batch.json",
    "instructions": "Return the complete JSON response without dropping records."
  },
  "providers": ["zyte"],
  "provider_options": {
    "zyte": {"browser_html": false}
  }
}
```

```bash
npx --yes @scrappycoco/cli@0.7.0 catalog inspect web.extract_content --json
npx --yes @scrappycoco/cli@0.7.0 run web.extract_content --file request.json --json
```

Use Discover when two or more available provider configurations need a paid,
same-input comparison. A configuration is a provider plus its native options.
Scrappycoco automatically adds a default candidate for each available provider
missing from the draft. The calling agent authors only materially different
option combinations that the goal makes relevant and judges all returned
evidence.

### Repeated-template batches

Treat a batch of pages that share one structure as one reusable-scraper
decision. If the exact provider/options configuration has not been validated
for that page family and requested output contract:

1. Bootstrap the directory with one bounded Run. Stop as soon as it yields at
   least one valid target-detail URL. Record a displayed total when cheaply
   available, but do not make complete enumeration a prerequisite for Discovery.
2. Run Discovery on that representative target page; use a second only for a
   material layout variant. Scrappycoco adds a default candidate for each
   available provider. Add explicit candidates only for materially different
   options relevant to the goal.
3. Judge page-sourced fields, representation, completeness, and truncation.
   Treat CAPTCHA, loading shells, invalid output, and timeouts as candidate
   failures. If a requested fact is absent from every complete source
   representation, prepare an enrichment route instead of asking a scraper to
   invent it.
4. Choose the strongest complete primary for the user's priority and preserve a
   passing different-provider fallback with its exact tested options.
5. Report the representative result and ask once before complete enumeration or
   batch execution. Use the source-reported count when available; an unknown
   count must not send the agent back into open-ended directory probing.
6. After confirmation, enumerate unique targets, establish the expected set or
   evidence basis, reconcile enumeration against any reported total, then
   execute the batch and enrichment and reconcile every target.

Discovery is the target-page difficulty test, not a reward for first solving
the entire directory. Configuration update and finalization are internal parts
of preflight, not additional user checkpoints. The calling agent remains free
to select capabilities and recovery methods from the live catalog.

```text
Extracted one representative exhibitor URL from the directory and tested 12
configurations on that detail page; 5 captured every page-sourced field.
Firecrawl structured is the strongest complete option and Zyte browser is the
tested fallback. The page reports about 924 exhibitors. LinkedIn is not present
on the representative source, so the full plan includes search enrichment.
Estimated remaining cost: about $4.20. Continue with complete enumeration and
the remaining batch? (yes/no)
```

Mention cost leadership only when comparison evidence supports it. The original
request authorizes the bootstrap and representative test; it does not authorize
complete enumeration or batch fan-out. Never ask whether to test, ask “sample or
all?”, offer sample sizes, or re-ask specified scope. Do not start, detach, or
queue the enumeration or batch while awaiting the answer. If declined, return
the representative result and comparison summary.

Declare a scalar page parameter such as `url` in the saved Discovery and test
the representative page. After finalization and confirmation, either invoke
that configuration per target or copy the exact primary and fallback options
into a supported batch Run. Do not silently return to curated defaults. Reuse
the sample only if its preserved result is equivalent to a finalized run.

Use the unique enumerated target set as the execution ledger. Reconcile the
target set with any source-reported total before the batch when possible. If the
reported total exceeds the unique URL count, enumeration is incomplete. Preserve
successful records, retry only unresolved targets with a materially changed
provider, options, input, or acquisition method, and use the tested fallback for
candidate-specific failures.
If failures reveal a systematic layout or navigation variant, re-Discover on a
failed representative. Never call a 50-of-150 result complete. If no
authoritative total exists, report the evidence used to conclude enumeration.

Skip this pattern for a small bounded one-off or when the exact configuration
was validated for the same page family and output contract. Merely receiving
`ok` from an unrelated page is not reusable validation.

## 2. Fill in a complete Discovery

Never leave `input_template` empty. Declare every runtime parameter and map it
into the capability input. Use one shared template for all candidates.

```json
{
  "goal": "Extract one company detail page completely and preserve its native links.",
  "priority": "quality",
  "configuration": {
    "name": "Company detail extraction",
    "summary": "Compare extraction configurations on one company detail URL.",
    "parameters": [
      {
        "name": "url",
        "label": "Company detail URL",
        "description": "Public company detail page to extract.",
        "type": "string",
        "required": true,
        "test_value": "https://example.com/companies/acme"
      }
    ],
    "routes": [
      {
        "id": "detail",
        "label": "Company detail",
        "purpose": "Return the visible company name, description, and website.",
        "source": "web",
        "capability": "extract_content",
        "input_template": {
          "url": "${url}",
          "instructions": "Return the visible company name, description, and website. Preserve native links. A loading shell is a failure."
        },
        "routing": "compare",
        "providers": [],
        "provider_options": {},
        "candidates": [
          {
            "id": "zyte-http",
            "provider": "zyte",
            "options": {"browser_html": false}
          },
          {
            "id": "zyte-browser",
            "provider": "zyte",
            "options": {"browser_html": true}
          },
          {
            "id": "firecrawl-markdown",
            "provider": "firecrawl_scrape",
            "options": {
              "formats": ["markdown", "links"],
              "only_main_content": true,
              "max_characters": 100000
            }
          },
          {
            "id": "firecrawl-json",
            "provider": "firecrawl_scrape",
            "options": {
              "formats": [
                {
                  "type": "json",
                  "prompt": "Return the visible company name, description, and website.",
                  "schema": {
                    "type": "object",
                    "properties": {
                      "company": {
                        "type": "object",
                        "properties": {
                          "name": {"type": "string"},
                          "description": {"type": "string"},
                          "website": {"type": "string"}
                        },
                        "required": ["name"]
                      }
                    },
                    "required": ["company"]
                  }
                }
              ],
              "only_main_content": true,
              "max_characters": 100000
            }
          }
        ]
      }
    ]
  }
}
```

Before saving, verify:

- `catalog inspect` confirms every capability, provider, and option.
- `parameters[].name` matches every `${parameter}` token.
- `input_template` satisfies the capability input schema after substitution.
- Every candidate receives the same resolved input.
- Candidate IDs are unique; the same provider should appear more than once
  when materially different native options could change success.
- Every candidate's options validate against the current `options_schema`.
  Choose formats, rendering, waits, actions, locale, and other exposed settings
  intentionally instead of accepting defaults without evaluation.
- Scrappycoco's normalized configuration contains a default candidate for every
  available provider. The draft only needs extra candidates for materially
  different provider modes relevant to the goal.
- The calling agent's evaluation rubric names the requested facts, required
  output representation, and explicit failure cases such as loading shells,
  missing rows, invalid JSON, absent HTML, or truncated content.
- When page behavior is uncertain, candidates span materially different
  provider classes such as HTTP, rendered, and browser-capable extraction.

## 3. Save and test

```bash
npx --yes @scrappycoco/cli@0.7.0 discover --file discovery.json --json
npx --yes @scrappycoco/cli@0.7.0 discover --id DISCOVERY_ID --test \
  --input '{"url":"https://example.com/companies/acme"}' \
  --output discovery-test.json --json
```

Run the test immediately. The output file contains the complete comparison
evidence while stdout remains a compact execution summary. The original data
request authorizes one representative test, and a second only for a material
layout variant, so do not ask for a budget, sample size, or permission first.
Ask the scale-up question after the primary, fallback, enrichment needs, and
post-confirmation enumeration plan are run-ready. After the test, inspect
`request_id`, every route attempt,
candidate ID, underlying provider ID, exact `provider_options`,
candidate-specific `provider_results`, each record's `primary_format` and
`outputs`, truncation metadata, and usage.

Provider status `ok` only means the request completed. The calling agent must
judge whether each candidate captures source-visible facts in the requested
representation. A Markdown response does not prove a JSON candidate works, and
a JSON response that fails its schema is not usable. A requested fact absent
from every complete source representation is an enrichment need, not permission
to invent a value or reject every otherwise-complete scraper.
If the resolved input is rejected, repair the configuration before drawing any
conclusion about provider quality. If all candidates fail the agent's rubric,
automatically search for a static page, public API, different capability, or
different provider class and use direct Run when the new configuration is
clear. Never generalize from an incomplete candidate set to “no provider can
scrape it.”

## 4. Select, update, and finalize

Replace the comparison route with one explicit winner and copy its exact
tested native options into `provider_options`. Send the complete configuration
in the update file; do not leave stale candidates behind or silently revert to
provider defaults.

This update/finalize sequence is an internal part of large-batch preflight, not
a user checkpoint. The finalized Discovery stores the primary. Separately
preserve the tested fallback's exact options. For a supported direct batch Run,
pass primary first and fallback second; never substitute an untested default.

```json
{
  "configuration": {
    "name": "Company detail extraction",
    "summary": "Extract a company detail page with the selected provider.",
    "parameters": [
      {
        "name": "url",
        "label": "Company detail URL",
        "description": "Public company detail page to extract.",
        "type": "string",
        "required": true
      }
    ],
    "routes": [
      {
        "id": "detail",
        "label": "Company detail",
        "purpose": "Return the visible company name, description, and website.",
        "source": "web",
        "capability": "extract_content",
        "input_template": {
          "url": "${url}",
          "instructions": "Return the visible company name, description, and website. Preserve native links."
        },
        "routing": "waterfall",
        "providers": ["zyte"],
        "provider_options": {
          "zyte": {"browser_html": true}
        },
        "candidates": []
      }
    ]
  }
}
```

```bash
npx --yes @scrappycoco/cli@0.7.0 discover --id DISCOVERY_ID \
  --update discovery-update.json --json
npx --yes @scrappycoco/cli@0.7.0 discover --id DISCOVERY_ID --finalize --json
npx --yes @scrappycoco/cli@0.7.0 run --config DISCOVERY_ID \
  --input '{"url":"https://example.com/companies/acme"}' --json
```

## 5. Report an auditable handoff

Before claiming completion, report:

- Scrappycoco request and Discovery IDs.
- Source URL and capability used.
- Selected candidate/provider and meaningful native options.
- Requested native output format and the keys present in `record.outputs`.
- Item counts, partial failures, retries, and truncation status.
- Actual usage/spend from the response.
- Any fallback source and whether it was also fetched through Scrappycoco.

Never say “through Scrappycoco” unless the corresponding response evidence was
preserved.
