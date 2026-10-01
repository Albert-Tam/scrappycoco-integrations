# Scrappycoco Agent Integrations

Coco is the public agent entry point; Scrappycoco supplies its tool infrastructure.

## Coco · Chief of Staff

`skills/coco` is the entry point. It greets the user, understands their goal and
hands sales and marketing work to the bundled VP of Sales and Chief Marketing Officer with the company, goal and mandate
intact. The specialist takes over in the same conversation without another
install, command or intake. All judgment stays in the user's AI client.

After publishing the distribution, paste this into your AI client:

```text
Install Coco, my Chief of Staff, using https://scrappycoco.ai/coco/install.md. Use one installation method, then read the coco skill and start in this conversation.
```

The portable installer selects only `coco`; the archive includes the specialist
and its guides. After publishing the integrations snapshot, Claude Code can use:

```sh
claude plugin marketplace add Albert-Tam/scrappycoco-integrations
claude plugin install coco@scrappycoco
```

Codex can use `codex plugin marketplace add
https://github.com/Albert-Tam/scrappycoco-integrations`, then
`codex plugin add coco@scrappycoco`. Use one installation method.

This plugin starts no server agent and requires no MCP authentication just to
onboard. Research uses a separately verified Scrappycoco connection when needed.
The marketplace exposes only `coco`; the public feed puts Coco first and retains
a legacy `scrappycoco` entry for older CLI installers. Legacy source packages and
archives remain for compatibility, but new users install the complete Coco package.
It bundles sales guidance and the Scrappycoco execution guide without additional
slash commands. See
`docs/coco-vp-sales.md` in the application repository for testing and rollout.

## Install

Paste this into your AI agent:

```text
Set up Scrappycoco: https://scrappycoco.ai/setup.md
```

CLI + Skill is the default. The setup guide detects the agent's execution
environment and uses the managed installer when Node/npm is missing. Customers
sign in in their browser; the agent installs the skill and verifies the catalog.
The agent reads the installed skill in the current conversation and can use the
CLI immediately. Automatic discovery for future sessions depends on the client.

For terminals with Node.js 20+, the npm shortcut remains available:

```sh
npx --yes @scrappycoco/cli@latest setup
```

## Optional MCP installation

Use <https://scrappycoco.readme.io/docs/mcp> when a client should expose
Scrappycoco tools natively through MCP.

Connect the remote server at `https://api.scrappycoco.ai/mcp` through the client's
native connector flow when needed. The Coco plugin does not force MCP or sign-in
for supplied-file work. The previous `scrappycoco` plugin is no longer advertised;
existing plugin installations are removed through their client's plugin manager,
not by the CLI migration.

## Install only Coco

```sh
npx --yes skills@latest add https://scrappycoco.ai --skill coco
```

Use the intended client and scope. The discovery feed at
`https://scrappycoco.ai/.well-known/agent-skills/index.json` advertises one
hash-verified archive with a single `SKILL.md`: `/coco`. The execution guide is
`tooling/scrappycoco/OPERATIONS.md`, not another discoverable skill.

## Replace an existing /scrappycoco installation

Use CLI 0.9.2 or newer and run `scrappycoco setup`. Setup reuses authentication,
installs Coco, then moves the active client's and shared legacy `scrappycoco`
skill directories into `skill-backups` beside `skills`. It preserves their files
and reports backup paths; other clients and unrelated skills are left alone.
The new CLI's skill updater also performs this migration on its next check.
A failed download/checksum check leaves the old command intact.

Older CLI binaries cannot migrate themselves; rerun the managed installer or
install the new npm release first. A merge/deployment does not remove files from
customer machines. Project-local skills and plugin-managed copies must be
removed or migrated in that same scope using the client's normal tools. Install
Coco successfully before retiring those copies. Refresh the command list as the
client requires; existing conversations may retain previously loaded instructions.
The executable remains `scrappycoco`, with the same auth, API, billing and tools.

The integration has two main actions:

- Discover: Scrappycoco runs explicit provider configurations on the same
  representative input and returns comparable evidence. The connected agent
  judges that evidence, selects the winner, and finalizes the configuration.
- Run: execute a saved configuration or call a known capability directly
  without rediscovering or reranking providers.

Scrappycoco does not act as another AI agent. All AI/LLM reasoning stays in the
user's agentic client—such as Cursor, Codex, or Claude—which owns semantic
interpretation, provider evaluation, configuration decisions, result judgment,
retry decisions, and monitoring schedules.

AI-powered providers may return assessments when selected for the user's task.
`ai.structured_judgment` supports classification and other typed judgments using
normal server credentials and billing. During a provider comparison, the client
may call it if the user asks, review its output alongside the original evidence,
and make the final decision. It has no mandatory consultation step.

Legacy server-side assistant, specialized-agent, workflow, and schedule tools are not
exposed.

On the first ordinary CLI command after a 24-hour cooldown, Scrappycoco compares
the installed skill release with the hash-verified public feed and refreshes it
automatically when the digest changes. The command continues if the check or
installer is unavailable. Read the updated skill in the current conversation
and continue using the CLI. Set
`SCRAPPYCOCO_SKILL_AUTO_UPDATE=0` to pin the installed copy and use `skill
update` for explicit checks. MCP-only users depend on their client or plugin
update flow. The skill never clones the private application repository.
