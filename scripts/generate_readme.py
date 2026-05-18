#!/usr/bin/env python3
"""Generate README.md from data/tools/*.yaml.

This repository intentionally keeps the registry as plain YAML cards without a
site build dependency. The parser below handles the small YAML subset used by
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
RISK_ORDER = ("low", "medium", "high")
RISK_LABEL = {"low": "Low", "medium": "Medium", "high": "High"}


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


def badge(label: str, message: str, color: str, href: str | None = None) -> str:
    image = f"https://img.shields.io/badge/{label}-{message}-{color}"
    markdown = f"![{label}: {message}]({image})"
    return f"[{markdown}]({href})" if href else markdown


def risk_badge(level: str) -> str:
    color = {"low": "2ea44f", "medium": "d29922", "high": "cf222e"}.get(level, "6e7781")
    return badge("risk", level, color)


def format_meta(tool: dict) -> str:
    parts = [f"`{tool['binary']}`", risk_badge(str(tool.get("risk_level") or "medium"))]
    langs = tool.get("lang") or []
    if langs:
        parts.append("lang: " + ", ".join(f"`{lang}`" for lang in langs[:4]))
    cats = tool.get("category") or []
    if len(cats) > 1:
        parts.append("also: " + ", ".join(f"`{cat}`" for cat in cats[1:4]))
    return " · ".join(parts)


def render_tool_line(tool: dict) -> str:
    name = md_escape(str(tool["name"]))
    summary = md_escape(str(tool.get("summary") or ""))
    href = link_for(tool)
    title = f"[{name}]({href})" if href else name
    meta = format_meta(tool)
    return f"- {title} — {summary}  \\\n  {meta}"


def render_category_card(category: str, tools: list[dict], risks: Counter[str]) -> str:
    high = risks.get("high", 0)
    medium = risks.get("medium", 0)
    low = risks.get("low", 0)
    if high:
        posture = "control plane"
    elif medium:
        posture = "operator surface"
    else:
        posture = "safe default"
    return (
        f"| [`{md_escape(category)}`](#{slugify(category)}) "
        f"| {len(tools)} | {low} | {medium} | {high} | {posture} |"
    )


def main() -> None:
    tools = sorted((parse_tool(path) for path in TOOLS_DIR.glob("*.yaml")), key=lambda item: str(item["name"]).lower())
    if not tools:
        raise SystemExit("No tool YAML files found in data/tools")

    category_groups: dict[str, list[dict]] = defaultdict(list)
    category_counts: Counter[str] = Counter()
    risk_by_category: dict[str, Counter[str]] = defaultdict(Counter)
    lang_counts: Counter[str] = Counter()
    risk_counts: Counter[str] = Counter()
    tool_by_name = {str(tool["name"]): tool for tool in tools}

    for tool in tools:
        categories = tool.get("category") or ["uncategorized"]
        risk_level = str(tool.get("risk_level") or "medium")
        for category in categories:
            category_groups[category].append(tool)
            risk_by_category[category].update([risk_level])
        category_counts.update(categories)
        lang_counts.update(tool.get("lang") or [])
        risk_counts.update([risk_level])

    risk_summary = " · ".join(f"{RISK_LABEL.get(risk, risk.title())}: **{risk_counts.get(risk, 0)}**" for risk in RISK_ORDER)
    top_categories = sorted(category_groups, key=lambda cat: (-len(category_groups[cat]), cat))[:8]

    lines: list[str] = []
    lines.extend(
        [
            '<div align="center">',
            "",
            "# Awesome Agent CLI",
            "",
            "**A machine-readable awesome list of CLI tools, risks, effects, and guardrails for AI coding agents.**",
            "",
            f"{badge('tools', str(len(tools)), '0969da')} {badge('categories', str(len(category_counts)), '8250df')} {badge('yaml', 'registry', '2ea44f')} [![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re) [![Update README](https://github.com/Ariestar/awesome-agent-cli/actions/workflows/update-readme.yml/badge.svg)](https://github.com/Ariestar/awesome-agent-cli/actions/workflows/update-readme.yml)",
            "",
            "</div>",
            "",
            "Awesome Agent CLI is a compact registry for teaching agents which command-line tools exist, what each tool is good for, and when a tool is risky enough to need extra care.",
            "Each entry is a plain YAML card under [`data/tools/`](data/tools/) so the registry is easy to diff, review, vendor, and consume from other projects.",
            "",
            "> [!NOTE]",
            "> This README is generated by [`scripts/generate_readme.py`](scripts/generate_readme.py). Edit the YAML cards, then regenerate the README instead of hand-editing the catalog sections.",
            "",
            "## Why this exists",
            "",
            "AI coding agents do not just need a list of binaries. They need operational context:",
            "",
            "- **When to use** a tool and when to avoid it.",
            "- **What side effects** the tool may have: file writes, network calls, auth, remote mutation, command execution.",
            "- **Which guardrails** are required before dangerous actions.",
            "- **How tools map** to categories like `shell`, `agent`, `mcp`, `security`, `deploy`, or `test`.",
            "",
            "## What's inside",
            "",
            "| Signal | Value |",
            "| --- | ---: |",
            f"| Tool cards | **{len(tools)}** |",
            f"| Category tags | **{len(category_counts)}** |",
            f"| Language/ecosystem tags | **{len(lang_counts)}** |",
            f"| Risk distribution | {risk_summary} |",
            "",
            "## Quick use",
            "",
            "```bash",
            "# Regenerate this README from the YAML registry",
            "python scripts/generate_readme.py",
            "",
            "# Inspect a card",
            "sed -n '1,120p' data/tools/gh.yaml",
            "```",
            "",
            "A tool card looks like this:",
            "",
            "```yaml",
            "name: gh",
            "binary: gh",
            "category:",
            "  - vcs",
            "  - ci",
            "risk:",
            "  level: high",
            "  effects:",
            "    - remote_read",
            "    - remote_write",
            "guardrails:",
            "  - Verify gh auth status before write operations.",
            "```",
            "",
            "## Agent workflow highlights",
            "",
            "These entries are especially useful when designing or hardening agent workflows:",
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
            "## Category map",
            "",
            "The matrix below shows category coverage and risk posture. A tool can appear in more than one category, so totals count category tags rather than unique files.",
            "",
            "| Category | Total | Low | Medium | High | Posture |",
            "| --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for category in sorted(category_counts):
        lines.append(render_category_card(category, category_groups[category], risk_by_category[category]))

    lines.extend(
        [
            "",
            "## Catalog",
            "",
            "Browse by category. Multi-category tools intentionally appear in every relevant section.",
            "",
            "<details open>",
            "<summary><strong>Popular categories</strong></summary>",
            "",
        ]
    )
    for category in top_categories:
        lines.append(f"- [`{category}`](#{slugify(category)}) — {len(category_groups[category])} tools")
    lines.extend(["", "</details>", ""])

    for category in sorted(category_groups):
        lines.append(f"### {category}")
        lines.append("")
        for tool in sorted(category_groups[category], key=lambda item: str(item["name"]).lower()):
            lines.append(render_tool_line(tool))
        lines.append("")

    lines.extend(
        [
            "## Maintaining the registry",
            "",
            "Add or edit a YAML card under [`data/tools/`](data/tools/). Keep entries short, factual, and operational:",
            "",
            "- describe the real command-line action surface an agent can call;",
            "- write `use_when` and `avoid_when` as decision rules, not marketing copy;",
            "- declare risk level and side effects honestly;",
            "- include guardrails for auth, secrets, network calls, writes, deployments, and destructive operations;",
            "- prefer official docs for `docs` or `homepage` links.",
            "",
            "> [!TIP]",
            "> If a tool can mutate remote state, expose secrets, execute generated code, or deploy infrastructure, mark it as high risk and add concrete guardrails.",
            "",
            "The GitHub workflow regenerates this README on pushes to `main` and checks generated output on pull requests.",
            "",
        ]
    )

    README.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
