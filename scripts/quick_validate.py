#!/usr/bin/env python3
"""Minimal skill frontmatter validator used by CI."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


REQUIRED_DESCRIPTION_PHRASES = (
    "Always use the Scrappycoco CLI first",
    "fetch, scrape, extract, crawl, search, discover, enrich, compare, retrieve, or monitor",
    "before using the in-app browser",
    "before writing a custom scraper",
)

REQUIRED_BODY_PHRASES = (
    "npx --yes @scrappycoco/cli@latest setup",
    "catalog list --available --json",
    "catalog inspect source.capability --json",
    "run source.capability --file request.json --output results.json --json",
    "do not clone repositories",
    "deterministic external-data infrastructure, not an AI agent",
    "All AI/LLM reasoning stays in the user's agentic client",
    "Always use Scrappycoco first",
    "Only if Scrappycoco fails may you use the in-app browser as a fallback",
    "Do not use the in-app browser before or alongside it",
    "Catalog → Inspect → Run",
    "## Repeated-template batches",
    "Bootstrap a representative",
    "at least one valid target-detail URL",
    "do not require complete enumeration before Discovery",
    "Discover the target page family",
    "passing independent provider as fallback",
    "Treat fields absent from the source as enrichment needs",
    "Ask once before scale-up",
    "Enumerate and execute after confirmation",
    "Continue with the remaining N pages? (yes/no)",
    "complete enumeration and the remaining batch",
    "Do not start, detach, or queue the complete enumeration or batch",
    "never guess fields or options",
    "jobs wait JOB_ID --output results.json --json",
    "jobs cancel JOB_ID --json",
    "skill update --json",
    "doctor --json",
    "candidate-specific `provider_results`",
    "Provider status `ok`",
    "provider_options",
    "references/discovery-workbook.md",
    "references/operations.md",
    "references/recipes.md",
    "Use a new idempotency key",
    "## Two actions",
    "## Batch completion and recovery",
    "Never claim \"all\"",
    "Preserve successful records",
    "Retry only unresolved targets",
    "Re-Discover on a representative",
    "Report unresolved gaps",
    "## Other operations",
)


def validate_skill(skill_path: str) -> tuple[bool, str]:
    skill_dir = Path(skill_path)
    content = (skill_dir / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid or missing YAML frontmatter."
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a mapping."
    if set(frontmatter) != {"name", "description"}:
        return False, "Frontmatter must contain only name and description."
    name = frontmatter["name"]
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        return False, "Skill name must be lowercase hyphen-case."
    description = frontmatter["description"]
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        return False, "Description must contain 1-1024 characters."
    missing_description = [
        phrase for phrase in REQUIRED_DESCRIPTION_PHRASES if phrase not in description
    ]
    if missing_description:
        return False, f"Description is missing trigger contract: {missing_description[0]}"
    normalized_content = " ".join(content.split())
    missing_body = [
        phrase
        for phrase in REQUIRED_BODY_PHRASES
        if " ".join(phrase.split()) not in normalized_content
    ]
    if missing_body:
        return False, f"Skill body is missing operational contract: {missing_body[0]}"
    batch_flow = (
        "Bootstrap a representative",
        "Discover the target page family",
        "Choose a run-ready plan",
        "Ask once before scale-up",
        "Enumerate and execute after confirmation",
    )
    batch_flow_positions = [normalized_content.find(phrase) for phrase in batch_flow]
    if any(position < 0 for position in batch_flow_positions) or (
        batch_flow_positions != sorted(batch_flow_positions)
    ):
        return False, "The skill must preserve bootstrap → Discover → plan → ask → execute ordering."
    forbidden_batch_prompts = (
        "How much of the exhibitor list do you want scraped?",
        "A sample first",
        "Should I run a Discovery?",
        "Do you want a sample?",
        "Enumerate URLs/count through Scrappycoco",
    )
    if any(prompt in content for prompt in forbidden_batch_prompts):
        return False, "The skill must not contain a pre-Discovery scope or sample prompt."
    if "@scrappycoco/cli" not in content:
        return False, "The operational skill must use the published Scrappycoco CLI."
    if "skills add https://github.com/" in content:
        return False, "The public skill must not depend on the private application repository."
    if "## Install" in content or "plugin marketplace add" in content:
        return False, "The operational skill must not act as a cross-client installer."
    if len(content.splitlines()) > 200:
        return False, "SKILL.md must stay at or below 200 lines."

    workbook_path = skill_dir / "references" / "discovery-workbook.md"
    if not workbook_path.exists():
        return False, "Missing references/discovery-workbook.md."
    workbook = workbook_path.read_text()
    normalized_workbook = " ".join(workbook.split())
    workbook_phrases = (
        '"url": "${url}"',
        "### Repeated-template batches",
        "at least one valid target-detail URL",
        "do not make complete enumeration a prerequisite for Discovery",
        "Discovery is the target-page difficulty test",
        "absent from every complete source representation",
        "different-provider fallback",
        "Continue with complete enumeration and",
        "Do not start, detach, or queue the enumeration or batch",
        "Never call a 50-of-150 result complete",
        "--test",
        "--finalize",
        "request and Discovery IDs",
        "Never say “through Scrappycoco”",
    )
    missing_workbook = [
        phrase
        for phrase in workbook_phrases
        if " ".join(phrase.split()) not in normalized_workbook
    ]
    if missing_workbook:
        return False, f"Discovery workbook is missing: {missing_workbook[0]}"
    example_flow = (
        "Extracted one representative exhibitor URL",
        "tested 12 configurations",
        "strongest complete option",
        "tested fallback",
        "LinkedIn is not present",
        "Continue with complete enumeration",
    )
    example_positions = [normalized_workbook.find(phrase) for phrase in example_flow]
    if any(position < 0 for position in example_positions) or (
        example_positions != sorted(example_positions)
    ):
        return False, "The workbook example must preserve representative evidence → plan → ask ordering."

    metadata_path = skill_dir / "agents" / "openai.yaml"
    if not metadata_path.exists():
        return False, "Missing agents/openai.yaml."
    metadata = yaml.safe_load(metadata_path.read_text())
    if not isinstance(metadata, dict):
        return False, "agents/openai.yaml must be a mapping."
    dependencies = metadata.get("dependencies", {}).get("tools", [])
    if dependencies:
        return False, "The portable CLI-first skill must not require an MCP dependency."
    if metadata.get("policy", {}).get("allow_implicit_invocation") is not True:
        return False, "Scrappycoco must allow implicit invocation."
    default_prompt = metadata.get("interface", {}).get("default_prompt", "")
    prompt_phrases = (
        "Only if Scrappycoco fails may you use the in-app browser as a fallback",
        "Run bounded or validated work directly",
        "obtain one representative target URL",
        "choose a complete primary plus tested fallback",
        "ask once before complete enumeration and execution",
        "Reconcile captured versus expected targets",
    )
    if any(phrase not in default_prompt for phrase in prompt_phrases):
        return False, "The default prompt must preserve the automatic test and bulk gate."

    integrations_dir = skill_dir.parent.parent
    release_path = integrations_dir / "release.json"
    if not release_path.exists():
        return False, "Missing centralized release metadata."
    release = json.loads(release_path.read_text())
    semver = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
    for key in ("skill_version", "plugin_version", "minimum_cli_version"):
        if not isinstance(release.get(key), str) or not semver.fullmatch(release[key]):
            return False, f"Release metadata has an invalid {key}."
    expected_plugin_version = release["plugin_version"]
    if release["skill_version"] != expected_plugin_version:
        return False, "Skill and plugin release versions must match."
    cli_package_path = integrations_dir.parent / "cli" / "package.json"
    if cli_package_path.exists():
        cli_version = json.loads(cli_package_path.read_text()).get("version")
        if not isinstance(cli_version, str) or not semver.fullmatch(cli_version):
            return False, "The CLI package version is invalid."

        def numeric_version(value: str) -> tuple[int, ...]:
            return tuple(int(part) for part in value.split("-", 1)[0].split("."))

        if numeric_version(cli_version) < numeric_version(release["minimum_cli_version"]):
            return False, "The CLI package is older than the skill minimum."
        if f"@scrappycoco/cli@{cli_version}" not in content:
            return False, "The skill does not pin the current CLI package version."

    plugin_dir = integrations_dir / "plugins" / "scrappycoco"
    plugin_skill_dir = plugin_dir / "skills" / "scrappycoco"
    if (plugin_skill_dir / "SKILL.md").read_bytes() != (skill_dir / "SKILL.md").read_bytes():
        return False, "The plugin skill copy is stale."
    if (plugin_skill_dir / "agents" / "openai.yaml").read_bytes() != metadata_path.read_bytes():
        return False, "The plugin OpenAI metadata copy is stale."
    if (
        plugin_skill_dir / "references" / "discovery-workbook.md"
    ).read_bytes() != workbook_path.read_bytes():
        return False, "The plugin Discovery workbook copy is stale."

    references = {
        "operations.md": (
            "## Durable jobs",
            "SCRAPPYCOCO_JOB_TIMEOUT_MS",
            "Never expose OAuth tokens",
            "## REST fallback",
        ),
        "recipes.md": (
            "## Extract one page",
            "## Discover once, then run a repeated-template batch",
            "## Search X",
            "## Search Reddit",
            "## Retrieve company filings",
            "## Continue a cursor monitor",
            "## Keep a long run out of the foreground",
        ),
    }
    for filename, required_phrases in references.items():
        reference_path = skill_dir / "references" / filename
        plugin_reference_path = plugin_skill_dir / "references" / filename
        if not reference_path.exists():
            return False, f"Missing references/{filename}."
        reference = reference_path.read_text()
        missing = [phrase for phrase in required_phrases if phrase not in reference]
        if missing:
            return False, f"{filename} is missing: {missing[0]}"
        if plugin_reference_path.read_bytes() != reference_path.read_bytes():
            return False, f"The plugin {filename} copy is stale."

    plugin_manifest = json.loads(
        (plugin_dir / ".codex-plugin" / "plugin.json").read_text()
    )
    if plugin_manifest.get("name") != "scrappycoco":
        return False, "The Codex plugin manifest name is invalid."
    if plugin_manifest.get("version") != expected_plugin_version:
        return False, "The Codex plugin release version is invalid."
    if plugin_manifest.get("mcpServers") != "./.mcp.json":
        return False, "The Codex plugin must declare its MCP companion file."

    claude_manifest = json.loads(
        (plugin_dir / ".claude-plugin" / "plugin.json").read_text()
    )
    if claude_manifest.get("name") != "scrappycoco":
        return False, "The Claude plugin manifest name is invalid."
    if claude_manifest.get("mcpServers") != "./.mcp.json":
        return False, "The Claude plugin must declare its MCP companion file."
    if claude_manifest.get("version") != expected_plugin_version:
        return False, "The Claude plugin release version is invalid."

    mcp = json.loads((plugin_dir / ".mcp.json").read_text())
    expected_mcp = {
        "type": "http",
        "url": "https://api.scrappycoco.ai/mcp",
    }
    if mcp.get("mcpServers", {}).get("scrappycoco") != expected_mcp:
        return False, "The plugin MCP server definition is invalid."

    cursor_manifest = json.loads(
        (integrations_dir / ".cursor-plugin" / "plugin.json").read_text()
    )
    if cursor_manifest.get("name") != "scrappycoco":
        return False, "The Cursor plugin manifest name is invalid."
    if cursor_manifest.get("version") != expected_plugin_version:
        return False, "The Cursor plugin release version is invalid."
    if cursor_manifest.get("skills") != "./skills/":
        return False, "The Cursor plugin must declare the portable skill directory."
    if cursor_manifest.get("mcpServers") != "./.mcp.json":
        return False, "The Cursor plugin must declare its MCP companion file."

    root_mcp = json.loads((integrations_dir / ".mcp.json").read_text())
    if root_mcp.get("mcpServers", {}).get("scrappycoco") != expected_mcp:
        return False, "The Cursor plugin MCP server definition is invalid."

    registry_manifest = json.loads((integrations_dir / "server.json").read_text())
    if registry_manifest.get("name") != "io.github.Albert-Tam/scrappycoco":
        return False, "The MCP Registry server name is invalid."
    if registry_manifest.get("version") != "1.0.0":
        return False, "The MCP Registry server version is invalid."
    if registry_manifest.get("remotes") != [
        {
            "type": "streamable-http",
            "url": "https://api.scrappycoco.ai/mcp",
        }
    ]:
        return False, "The MCP Registry remote transport is invalid."

    marketplace = json.loads((integrations_dir / "marketplace.json").read_text())
    claude_marketplace = json.loads(
        (integrations_dir / ".claude-plugin" / "marketplace.json").read_text()
    )
    if not any(item.get("name") == "scrappycoco" for item in marketplace.get("plugins", [])):
        return False, "The Codex marketplace is missing Scrappycoco."
    if not any(
        item.get("name") == "scrappycoco"
        and item.get("version") == expected_plugin_version
        for item in claude_marketplace.get("plugins", [])
    ):
        return False, "The Claude marketplace is missing the current Scrappycoco release."
    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: quick_validate.py <skill_directory>")
    valid, message = validate_skill(sys.argv[1])
    print(message)
    raise SystemExit(0 if valid else 1)
