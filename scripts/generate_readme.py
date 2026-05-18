#!/usr/bin/env python3
"""Generate README.md from data/tools/*.yaml.

This repository intentionally keeps the registry as plain YAML cards without a
site build dependency.  The parser below handles the small YAML subset used by
our tool cards so the README workflow can run with only the Python standard
library.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "data" / "tools"
README = ROOT / "README.md"
LIST_KEYS = {"aliases", "category", "lang", "platform", "use_when", "avoid_when", "guardrails"}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9 -]", "", value)
    value = value.replace(" ", "-")
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def clean_scalar(value: str) -> str | list[str]:
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [clean_scalar(part.strip()) for part in inner.split(",")]  # type: ignore[list-item]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return value


def parse_tool(path: Path) -> dict:
    tool: dict = {"aliases": [], "category": [], "lang": [], "platform": []}
    current_key: str | None = None
    in_risk = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if line.startswith("- ") and current_key in LIST_KEYS:
            item = clean_scalar(line[2:])
            if isinstance(item, str):
                tool.setdefault(current_key, []).append(item)
            continue

        if indent == 0:
            in_risk = False
            if line.endswith(":"):
                current_key = line[:-1]
                if current_key in LIST_KEYS:
                    tool[current_key] = []
                if current_key == "risk":
                    tool["risk"] = {}
                    in_risk = True
                continue

            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            parsed = clean_scalar(value)
            tool[key] = parsed
            current_key = key
            continue

        if current_key == "risk" and ":" in line:
            key, value = line.split(":", 1)
            tool.setdefault("risk", {})[key] = clean_scalar(value)
            in_risk = True
            continue

        # Keep enough state to ignore nested detect fields without accidentally
        # appending their list items to top-level fields.
        if indent > 0 and line.endswith(":") and not in_risk:
            current_key = None

    tool["slug"] = path.stem
    tool.setdefault("name", path.stem)
    tool.setdefault("binary", tool["name"])
    tool.setdefault("summary", "")
    tool.setdefault("homepage", "")
    tool.setdefault("docs", "")
    tool.setdefault("category", [])
    tool.setdefault("lang", ["all"])
    tool.setdefault("platform", [])
    tool.setdefault("aliases", [])
    if isinstance(tool.get("risk"), dict):
        tool["risk_level"] = tool["risk"].get("level", "medium")
    else:
        tool["risk_level"] = "medium"
    return tool


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def link_for(tool: dict) -> str:
    return str(tool.get("docs") or tool.get("homepage") or "").strip()


def format_meta(tool: dict) -> str:
    parts = [f"`{tool['binary']}`"]
    risk = tool.get("risk_level")
    if risk:
        parts.append(f"risk: `{risk}`")
    langs = tool.get("lang") or []
    if langs:
        parts.append("lang: " + ", ".join(f"`{lang}`" for lang in langs))
    cats = tool.get("category") or []
    if len(cats) > 1:
        parts.append("also: " + ", ".join(f"`{cat}`" for cat in cats[1:]))
    return " · ".join(parts)


def render_tool_line(tool: dict) -> str:
    name = md_escape(str(tool["name"]))
    summary = md_escape(str(tool.get("summary") or ""))
    href = link_for(tool)
    title = f"[{name}]({href})" if href else name
    meta = format_meta(tool)
    return f"- {title} — {summary}  \\\n  {meta}"


def main() -> None:
    tools = sorted((parse_tool(path) for path in TOOLS_DIR.glob("*.yaml")), key=lambda item: str(item["name"]).lower())
    if not tools:
        raise SystemExit("No tool YAML files found in data/tools")

    category_groups: dict[str, list[dict]] = defaultdict(list)
    category_counts: Counter[str] = Counter()
    lang_counts: Counter[str] = Counter()
    risk_counts: Counter[str] = Counter()
    tool_by_name = {str(tool["name"]): tool for tool in tools}

    for tool in tools:
        categories = tool.get("category") or ["uncategorized"]
        for category in categories:
            category_groups[category].append(tool)
        category_counts.update(categories)
        lang_counts.update(tool.get("lang") or [])
        risk_counts.update([tool.get("risk_level") or "medium"])

    lines: list[str] = []
    lines.extend(
        [
            "# Awesome Agent CLI",
            "",
            "> A curated, machine-readable registry of command-line tools and action surfaces for AI coding agents.",
            "",
            "[![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)",
            "[![Update README](https://github.com/Ariestar/awesome-agent-cli/actions/workflows/update-readme.yml/badge.svg)](https://github.com/Ariestar/awesome-agent-cli/actions/workflows/update-readme.yml)",
            "",
            "This repository stores one YAML card per CLI tool in [`data/tools/`](data/tools/).",
            "Each card describes when an agent should use the tool, when to avoid it, and which risks or side effects require guardrails.",
            "",
            "<!-- This README is generated by scripts/generate_readme.py. Do not edit the tool list by hand. -->",
            "",
            "## Contents",
            "",
        ]
    )

    for category in sorted(category_groups):
        lines.append(f"- [{category}](#{slugify(category)}) ({len(category_groups[category])})")

    lines.extend(
        [
            "",
            "## Registry at a glance",
            "",
            f"- **Tools:** {len(tools)}",
            f"- **Categories:** {len(category_counts)}",
            f"- **Languages/ecosystems:** {len(lang_counts)}",
            f"- **Risk levels:** " + ", ".join(f"`{risk}` {count}" for risk, count in sorted(risk_counts.items())),
            "",
            "## Featured agent workflow tools",
            "",
            "A short starting set for agent-oriented shell work, repository context packaging, MCP debugging, and CI/security hygiene.",
            "",
        ]
    )

    featured = [
        "bash", "pwsh", "tmux", "pueue",
        "crush", "repomix", "files-to-prompt", "llm",
        "mcp-inspector", "mcp-proxy",
        "actionlint", "zizmor", "detect-secrets", "osv-scanner",
    ]
    for name in featured:
        if name in tool_by_name:
            lines.append(render_tool_line(tool_by_name[name]))
    lines.extend(
        [
            "",
            "## Tools",
            "",
        ]
    )

    for category in sorted(category_groups):
        lines.append(f"### {category}")
        lines.append("")
        for tool in sorted(category_groups[category], key=lambda item: str(item["name"]).lower()):
            lines.append(render_tool_line(tool))
        lines.append("")

    lines.extend(
        [
            "## Category index",
            "",
            "Tools can belong to multiple categories, so a tool may appear in more than one section. This index counts every category tag.",
            "",
            "| Category | Tools |",
            "| --- | ---: |",
        ]
    )
    for category, count in sorted(category_counts.items()):
        lines.append(f"| `{md_escape(category)}` | {count} |")

    lines.extend(
        [
            "",
            "## Contributing",
            "",
            "Add or edit a YAML card under [`data/tools/`](data/tools/). A good entry should:",
            "",
            "- describe a real command-line action surface an agent can call;",
            "- explain `use_when` and `avoid_when` in operational terms;",
            "- declare risk level and effects honestly;",
            "- include guardrails for writes, network access, auth, secrets, deployment, or destructive operations;",
            "- link to official docs or the best available reference.",
            "",
            "After changing YAML cards, run:",
            "",
            "```bash",
            "python scripts/generate_readme.py",
            "```",
            "",
            "The GitHub workflow also regenerates this README automatically on pushes to `main` and checks it on pull requests.",
            "",
        ]
    )

    README.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
