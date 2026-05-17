# Awesome Agent CLI

CLI tools that make AI coding agents more capable, safer, and faster.

Not just links — action metadata with risk, guardrails, and effects.

## What is this?

A curated registry of CLI/action tools that AI coding agents can actually use. Each tool entry includes:

- **use_when** — when an agent should pick this tool
- **avoid_when** — when another tool is better
- **guardrails** — safety rules for agents
- **risk** — low / medium / high / critical
- **effects** — read_files, write_files, execute_code, network_access, etc.

## Browse

Visit the website or use the JSON API:

```
public/data/tools.json
```

## Use with Runbook CLI

```bash
runbook scan
runbook category search --lang rust
runbook category test --lang python
```

## Contribute

Add a YAML file to `data/tools/your-tool.yaml`. See [/contribute](/contribute) for the template and field reference.

## Development

```bash
pnpm install
pnpm dev       # dev server at localhost:4321
pnpm build     # static build to dist/
pnpm preview   # preview the build
```

## Tech Stack

- [Astro](https://astro.build) — static site framework
- [React](https://react.dev) — interactive search island
- [Tailwind CSS](https://tailwindcss.com) — styling
- Tool data: YAML files in `data/tools/`

## License

ISC
