# MCP-only operation

CLI + Skill is the default for terminal-capable clients. Use this reference only
when local execution is unavailable or the customer explicitly chose MCP.
Use the authenticated remote server at `https://api.scrappycoco.ai/mcp`.
Do not install Node, npm, or a CLI to use tools that are already connected.

Read the exposed tool schemas before supplying arguments. The same Discover and
Run evidence rules apply to every interface:

| CLI operation | MCP tool |
| --- | --- |
| catalog list | list_scrapers |
| catalog inspect | get_scraper |
| run a capability | run_scraper |
| same-input comparison | compare_scrapers |
| create a Discovery | discover_scrapers |
| inspect/update/finalize a Discovery | get_discovery / update_discovery / finalize_discovery |
| run a saved Discovery | run_discovery |
| submit/wait/cancel a durable job | submit_scraper_job / get_job / cancel_job |

Let the calling AI choose providers and exact native options, judge requested
fields, relevance, representation, errors, and truncation, then compare cost
only among equally satisfactory results. Never treat transport success as proof
of usefulness. Preserve native outputs, candidate evidence, and independent
passing fallbacks under the same rubric as CLI workflows.

Verify connection with `list_scrapers`. Follow the client's OAuth flow if
authentication is needed. Never request tokens or keys in chat.
