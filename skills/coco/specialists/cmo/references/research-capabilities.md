# Map marketing outcomes to verified tools

The live catalog and inspected schemas are authoritative. These IDs are lookup
hints grounded in the repository catalog, not guarantees of deployed availability.
Read the installed execution guide for CLI/MCP setup and exact requests. Inspect
only relevant families; never run the whole catalog because it is available.

```bash
scrappycoco catalog list --source social --json
scrappycoco catalog inspect social.discover_hooks --json
scrappycoco catalog list --source company --json
scrappycoco catalog list --source people --json
```

Use unfiltered listings to distinguish unavailable capabilities from absent ones.
Check each provider's availability, schema, native options, price evidence and
pagination before execution. Retain full response receipts. Search snippets and
provider judgments are evidence to assess, not verified claims by themselves.

| Marketing outcome | Capabilities to inspect | Deliverable and evidence boundary |
| --- | --- | --- |
| Creator partnerships | `social.find_micro_influencers`, `social.creator_contacts`; Instagram/TikTok `search_profiles`, `similar_profiles`, `profile`, `connected_socials` where present | Shortlist with audience-fit evidence, recent examples, dates, public business contact source and unknowns. No invented rates, demographics or willingness. |
| TikTok/Reels hooks | `social.discover_hooks`, `social.find_winning_videos`; `tiktok.search_posts`, relevant transcripts/account posts | Exact observed opening with URL, date and medium; separate proposed adaptations. Public views do not prove conversion. |
| LinkedIn publishing and audience development | `linkedin.profile`, `linkedin.company_profile`, `linkedin.account_posts`, `linkedin.company_posts`, `linkedin.search_posts`, `linkedin.post`, `linkedin.post_comments` | Profile edits, original post drafts, editorial calendar and contextual public replies informed by dated evidence. These are read capabilities; publishing, profile updates and scheduling require separate verified client tools. |
| Meta creative | `social.meta_ad_inspiration`, `social.score_accounts`, relevant social posts/transcripts | Hook, opening shot, storyboard, body copy, CTA, placement and test hypothesis. This is inspiration, not Meta Ad Library coverage or campaign activation. |
| Trends and voice of customer | `social.find_trending_topics`, `reddit.search_posts`, `reddit.post_comments`, `x.search_posts`, `web.search_web` | Dated independent examples, audience language and uncertainty. Reposts are not independent evidence; recent is not necessarily rising. |
| Positioning and competitive research | `web.search_web`, `web.extract_content`, `web.crawl_site`, `web.map_links`, `web.screenshot`; company enrichment | Evidence matrix of audience, offer, claims, pricing and differentiation, followed by original positioning. Respect source dates and incomplete pages. |
| SEO and answer visibility | `web.search_web`, extraction/crawl; `web.ask_chatgpt`, `web.ask_copilot`, `web.ask_perplexity`, `web.ask_gemini`, `web.ask_google_ai_mode`, `web.ask_grok` | Query/engine/date-specific observations and cited content gaps. Availability varies; one answer is not search market share or a ranking guarantee. |
| B2B audience and account-based marketing | `company.search_records`, `company.find_similar`, `company.enrich_domain`, `company.workforce`; Coresignal `company.search`, `company.preview`, `company.collect` | Evidence-backed audience segments and account shortlist. Native lookalike ranks are provider output for the client to judge; workforce growth is not buying intent. |
| B2B contacts and sales handoff | `people.search`, `people.get_record`, `people.lookup_email`, `people.email`; `employee.search`, `employee.collect` | Current role/company evidence and native email status/certainty when available. An address is not outreach permission or a guaranteed deliverable mailbox. |
| Market signals | `jobs.search`, `jobs.collect`, filings capabilities, company workforce | Dated hiring/regulatory signals with status; do not turn a vacancy into budget or infer causation. |
| Repeated checks | Relevant `monitor` capabilities | One-shot evidence with saved cursor; caller owns requested scheduling. |

## Turn available connections into task suggestions

Use the relevant rows above after checking live provider availability and the
client's connected app actions. Suggest only the supported part of the workflow;
do not assume a social research connection can also publish or buy ads. Adapt
these examples to the company, goal and verified access:

| Verified access | Example suggestion |
| --- | --- |
| Creator discovery and Instagram/TikTok profile research | “Find five creators in your niche, check recent content for fit, and prepare a partnership shortlist and brief.” |
| TikTok/Reels posts, videos or hook research | “Research five relevant short-form openings and write three original scripts for your product.” |
| Meta creative inspiration | “Research relevant creative patterns and draft three Meta ad concepts with copy, opening shots and a test plan.” |
| LinkedIn research | “Review recent audience conversations and draft three LinkedIn posts with supported claims.” |
| Connected social publishing/scheduling actions | “Prepare a week of posts for your connected account, then publish or schedule within your mandate.” |
| Connected ads reporting or supplied performance exports | “Compare recent campaigns using actual spend and conversion data, then propose the next creative test.” |
| Connected campaign creation/management actions | “Prepare the campaign settings and creative for your connected ad account, then activate within your authorized budget and scope.” |

These are conditional examples, not a fixed integration inventory. Resolve the
client's actual app and account access before naming it as connected. Keep
research access, reporting access and mutation access distinct. If discovery is
unavailable, disclose the unverified dependency briefly and propose a deliverable
that can be completed from the supplied context. Do not claim audience fit or
campaign performance until the evidence has been acquired and assessed.

For social research, read the execution guide's social cookbook. Include actual
product and audience, platform, resolved date window, desired count and source
requirements in the provider question. Keep research platform separate from ad
destination. Preserve exact sourced text; identify speech, captions and on-screen
text. Mark translations and rewrites. Ask for complete entries rather than
unaligned parallel arrays.

For CompanyEnrich, read the execution guide's CompanyEnrich reference. Inspect
filters and reference lookups rather than guessing industry, seniority or size
enums. Coresignal IDs and CompanyEnrich IDs are different namespaces. Previews
may be plan-restricted; a denied preview does not disable paid search. Prefer a
bounded known search over a broad export. Account lists/jobs are owner-only;
customer workflows must not try to inspect the provider's shared account.

No listed capability promises ad purchasing, social publication, attribution,
email campaigns, image/video generation or marketing automation. Use verified
client tools for those steps under the user's mandate. If missing, complete the
research and drafts and say exactly what remains to execute.
