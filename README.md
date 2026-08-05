# Scrappycoco Agent Integrations

Official agent skill and integration metadata for Scrappycoco.

## Install

For coding agents, run:

```sh
npx --yes @scrappycoco/cli@latest setup
```

This is the recommended path. It opens browser sign-in or account creation,
stores OAuth credentials securely, installs the portable skill, and verifies
the live catalog. Reload or restart an agent that was already running.

Users can paste this into a terminal-capable coding agent:

```text
Run npx --yes @scrappycoco/cli@latest setup and guide me through browser sign-in or account creation. Do not report success until setup verifies the live catalog. Then reload the installed Scrappycoco skill and use its CLI-first workflow.
```

## Optional MCP installation

Use <https://scrappycoco.ai/install#mcp> when a client should expose
Scrappycoco tools natively through MCP.

Codex CLI and desktop app:

```sh
codex plugin marketplace add https://github.com/Albert-Tam/scrappycoco-integrations
codex plugin add scrappycoco@scrappycoco
```

Claude Code:

```sh
claude plugin marketplace add Albert-Tam/scrappycoco-integrations
claude plugin install scrappycoco@scrappycoco
```

When installing during a running Claude Code session, run `/reload-plugins`,
then `/mcp`, select `scrappycoco`, and complete authentication. Claude Code does
not launch MCP OAuth as part of `claude plugin install`.

The plugin packages the portable skill and remote MCP connection together.
Client reload, trust, and OAuth approval remain explicit security steps.

## Install only the portable skill

```sh
npx --yes skills@latest add https://scrappycoco.ai \
  --skill scrappycoco -g -y
```

The CLI setup command installs from the public Agent Skills discovery feed at
`https://scrappycoco.ai/.well-known/agent-skills/index.json`. It distributes a
hash-verified archive containing the portable CLI-first skill without exposing
the private application repository or requiring MCP.

The plugin under `plugins/scrappycoco` packages the same skill with the remote
Streamable HTTP MCP server at `https://api.scrappycoco.ai/mcp`. The distribution
has Codex/OpenAI, Claude Code, and Cursor metadata. `server.json` is the
canonical official MCP Registry manifest. The npm CLI is documented separately.

The integration has two main actions:

- Discover: Scrappycoco runs explicit provider configurations on the same
  representative input and returns comparable evidence. The connected agent
  judges that evidence, selects the winner, and finalizes the configuration.
- Run: execute a saved configuration or call a known capability directly
  without rediscovering or reranking providers.

Scrappycoco does not act as another AI agent. All AI/LLM work stays in the
user's agentic client—such as Cursor, Codex, or Claude—which owns semantic
interpretation, provider evaluation, configuration decisions, result judgment,
retry decisions, and monitoring schedules.

Legacy assistant, specialized-agent, workflow, and schedule tools are not
exposed.

On ordinary CLI commands, Scrappycoco compares the installed skill release with
the hash-verified public feed and refreshes it automatically when the digest
changes. The current agent must still be reloaded or restarted before it can use
the new instructions. MCP-only users depend on their client or plugin update
flow. The skill never clones the private application repository.
