# Social research cookbook

Use this reference when a user wants social video examples, account feedback,
hooks, creators, trends, ad inspiration or public creator business contacts.
The calling AI authors the question and judges the returned evidence. Lightreel
is the external research provider; Scrappycoco transports the exact question
without adding prompts or choosing which findings are useful.

## Build the brief before Run

Reuse relevant facts already provided in the conversation. Include the actual
product, audience, differentiator and desired outcome, not just its brand name.
If the product or target account is missing and cannot be inferred, ask one
focused question before spending a request. Do not invent the missing niche.
For optional details, use reasonable assumptions and state them; do not turn a
small research request into an intake questionnaire.

Include the requested platform, region/language when relevant, explicit date
window and desired count. Resolve relative dates using the current date; never
reuse the dates in an old example. Keep research platform and advertising
destination distinct: Instagram-only research must not silently become TikTok
research just because the destination is Meta ads. Include previous creative
results and brand constraints only when the user actually supplied them.

Choose breadth versus depth deliberately. Five well-supported examples may
serve an ad brief better than an unsupported list of fifty. Do not automatically
run all seven capabilities: choose the one matching the user's task.

## Shared evidence requirements

Append requirements appropriate to the task, using this as a starting point:

> Support each finding with a direct post or profile URL. Include the creator,
> publication date when verified, available engagement metrics and the date of
> observation. Mark missing facts unknown; never invent links, quotations,
> dates, metrics or contacts. Separate direct observations, provider inference
> and proposed adaptations. Explain missing evidence and any departure from the
> requested platform, niche, dates or count.

Ask for exact source words only when directly observed, distinguishing speech,
on-screen text and captions. Preserve the original language, punctuation and
emoji; label translations and rewritten hooks separately. A link returned by
the provider is a citation to examine, not proof that it was independently
verified by the calling agent.

## Choose and adapt a recipe

Replace bracketed slots with the user's context before sending. These are
starting briefs, not guaranteed high-performing prompts. Add the shared evidence
requirements and task-specific output fields. Each recipe below is an adaptation
of the linked official example, with additional evidence checks.

### Find winning videos — `social.find_winning_videos`

> Research [count] videos on [platform] for [accounts or niche] published between
> [start] and [end]. Identify unusually strong performance using [user's metric
> or an explicitly stated comparison]. Compare against the creator's recent
> baseline where data permits. Describe the opening, editing and format changes,
> with the underlying metrics and source examples. Explain alternative reasons
> for an apparent improvement. If baseline data is unavailable, report observed
> engagement without claiming a breakout or a cause.

Request entries containing the video URL, creator, dates, metrics, baseline,
observed change and limitations. Views alone do not establish conversion or
causal effectiveness. [Official example](https://lightreel.ai/docs/examples/find-winning-videos).

### Score accounts — `social.score_accounts`

> Review [exact account URLs] for [audience and business objective], using posts
> from [date window]. Evaluate [user's criteria] with specific post examples.
> If scores are requested, define the scale and explain each score from observed
> evidence. Separate strengths, weaknesses and concrete changes to test. Mark
> criteria that cannot be assessed from public data as unknown.

Use one feedback entry per account. If the user supplied no rubric, state a
task-relevant one such as opening clarity, editing, consistency and CTA before
applying it. Scores are provider opinions for the calling agent to assess.
[Official example](https://lightreel.ai/docs/examples/score-and-critique-accounts).

### Discover hooks — `social.discover_hooks`

> Our product is [description and differentiator] for [audience]. Research
> [count] opening hooks used by [competitors or adjacent niche] on [platform]
> during [date window]. Give the observed wording, its medium, the source video,
> product and supporting performance evidence. Explain the cultural or format
> context with dated examples. Separately propose [count] adaptations for our
> product, each linked to the source pattern. Examine word choice, punctuation,
> emoji and opening visual; avoid additions that do not serve the idea. Explain
> plausible variations and what an actual test would need to establish.

Keep sourced hooks and proposed hooks in separate fields. Neither a large view
count nor reasoning about alternatives makes an adaptation battle-tested.
Only use that label when actual relevant testing evidence exists.
[Official example](https://lightreel.ai/docs/examples/discover-hooks).

### Find micro-influencers — `social.find_micro_influencers`

> Find [count] creators on [platform] serving [audience/niche/region/language]
> with [follower range]. Prioritize [breadth or depth] for [campaign objective].
> Return profile URLs, follower counts with observation dates, recent relevant
> posts and evidence of audience fit. Cite any past brand partnerships; mark
> partnership status or willingness to work with brands unknown without evidence.
> Identify which criteria each creator meets and any that could not be checked.

Do not infer audience demographics from appearance or equate a business email
with availability. Missing partnership evidence is not proof of no partnerships.
[Official example](https://lightreel.ai/docs/examples/find-micro-influencers).

### Find trending topics — `social.find_trending_topics`

> Research [niche] on [platform] between [start] and [end], for [audience and use].
> Group [count] topics with supporting post URLs and publication dates. Explain
> whether each is a newly observed topic, recurring discussion or a measurable
> rise against [comparison period]. Provide independent examples and comparable
> metrics when available. Distinguish the event date from its coverage date and
> avoid counting reposts as independent corroboration. State coverage gaps.

A single recent post is not sufficient evidence of a trend. Do not claim an
exhaustive scan without a known universe and reconciled results. A one-time Run
does not set up ongoing alerts.
[Official example](https://lightreel.ai/docs/examples/find-trending-topics).

### Instagram/Meta ad inspiration — `social.meta_ad_inspiration`

> Find [count] real [research platform] videos from [date window] to inspire
> [ad placement] ads for [product, audience and differentiator]. Our known
> creative results are [only supplied results; omit if unknown]. Seek specific
> emerging formats and details useful to an editor. For each, give the URL,
> observed opening, visual sequence, available metrics and why it might fit our
> product. Label organic examples and verified paid ads separately. Then propose
> [count] untested adaptations with a hook, opening shot, sequence and CTA,
> each connected to the researched examples. Explain where the evidence is weak.

Organic engagement does not demonstrate ROAS, CAC or winning paid distribution.
This capability does not promise Meta Ad Library coverage. If the user needs
verified running ads, inspect the catalog for that evidence; do not substitute
organic videos without making the gap explicit.
[Official example](https://lightreel.ai/docs/examples/meta-ad-inspiration).

### Public creator contacts — `social.creator_contacts`

> Find [count] creators matching [criteria] on [platform] for [business purpose].
> Return the handle, profile URL and publicly listed business contact, with the
> exact page that publishes it and observation date. Distinguish creator and
> agency contacts. Mark unavailable contacts unknown, deduplicate entries and
> include evidence that each creator meets the requested criteria. Do not guess
> email addresses or imply that an address was deliverability-tested.

Return one complete entry per creator to preserve contact attribution.
[Official example](https://lightreel.ai/docs/examples/pull-creator-contacts).

## Send the request

Inspect the selected capability before execution. If it is unavailable or absent
from the live catalog, report that; an installed recipe does not enable a route.

```bash
scrappycoco catalog inspect social.discover_hooks --json
```

A complete example request file, with illustrative product context:

```json
{
  "source": "social",
  "capability": "discover_hooks",
  "input": {
    "question": "Find 5 Instagram Reel hooks for a screen-time app that asks users to exercise before opening distracting apps. The audience is adults seeking less scrolling. Focus on the last 7 days and state the date window used. Return exact observed hook wording with its medium, source Reel URL, creator, publication date when known and available engagement with observation date. Mark missing data unknown and label any older or adjacent examples. Separately propose 3 untested adaptations, each linked to a source example. Preserve source punctuation and emoji; label all rewrites. Do not invent quotations or metrics, or imply paid-ad or conversion performance. Explain cultural context and limitations using dated sources."
  },
  "providers": ["lightreel"],
  "provider_options": {
    "lightreel": {
      "response_fields": {
        "evidence": {
          "type": "array",
          "description": "One complete entry per sourced hook: observed text and medium, video URL, creator, publication date, metrics and observation date, context and unknown fields."
        },
        "adaptations": {
          "type": "array",
          "description": "Untested proposed hooks, each with source URLs, proposed wording, opening visual, rationale, variations and what still needs testing."
        },
        "limitations": {
          "type": "string",
          "description": "Missing evidence, the date window used, deviations from requested scope, and verification limits."
        }
      }
    }
  }
}
```

Save the completed JSON as `request.json`. Use durable execution for slow runs:

```bash
scrappycoco run social.discover_hooks --file request.json --detach --json
scrappycoco jobs wait JOB_ID --output hooks.json --json
```

Structured output is optional. When used, `response_fields` supports one to five
fields, each typed `string` or `array`; it is not a general JSON Schema. Put
requested evidence in the descriptions. Prefer complete entries over parallel
arrays; if parallel arrays are useful, explicitly request matching indexes and
check alignment on receipt. The gateway does not enforce nested entry structure.
One normalized record holds the whole answer. Put counts in the question, not
the gateway `limit`. See the [official output contract](https://lightreel.ai/docs).

For MCP, inspect with `get_scraper` and use the same `input`, `providers` and
`provider_options` with `scraper_id: "social.discover_hooks"`; follow the exposed
job schemas for long runs. REST uses the same request JSON. Each request must
carry its own relevant brief and supplied context.

## Evaluate before reporting

Read the saved answer, not just the execution summary. Check requested count,
platform, date window, relevance and field completeness; keep native evidence.
Reject invented-looking placeholders as unsupported. State when source links or
metrics have not been independently verified. If stronger verification matters,
inspect available source-fetching tools and verify claims within the user's
scope and request budget; do not silently launch more paid research calls.

Do not turn an unsupported provider judgment into a fact, or interpret `ok` as
proof of quality. Return usable findings with their limitations. For competing
configurations, the calling AI judges task satisfaction before comparing cost.
Follow the main skill's Discovery rules if a further acquisition is needed and
provider or configuration choice remains uncertain.

Inspect current pricing before execution. Under the initial configured rate,
each completed Lightreel request costs $0.50, including each separate batch item
or comparison candidate; a list of five examples inside one answer is one
request. Transport timeouts can leave provider usage unknown. Wait for an
existing job instead of submitting duplicate research. Prompt guidance improves
specificity and auditability; it cannot guarantee factual or creative quality.
