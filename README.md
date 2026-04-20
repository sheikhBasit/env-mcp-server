# env-mcp-server

Environment & secrets inspector MCP server — read, validate, and diff `.env` files.

## Tools

| Tool | Description |
|---|---|
| `read` | Read a `.env` file — secrets masked by default |
| `validate` | Check `.env` against `.env.example` — missing, extra, empty vars |
| `diff` | Compare two `.env` files side-by-side |
| `missing` | List required vars missing from your `.env` |

## Quick Start

```bash
git clone https://github.com/sheikhBasit/env-mcp-server
cd env-mcp-server
python -m venv .venv && .venv/bin/pip install -e .
env-mcp
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "env": {
      "command": "/path/to/.venv/bin/env-mcp"
    }
  }
}
```

## Usage Examples

```
read my .env file at /app/.env
validate /app/.env against /app/.env.example
diff /app/.env.dev and /app/.env.prod
what vars am I missing in /app/.env?
```

## Security

Secrets are masked by default — any key matching `secret`, `password`, `token`, `key`, `api_key`, `jwt`, etc. returns `***MASKED***`. Pass `mask_secrets=false` to see raw values.

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT


---

## Knowledge Graph

This repo is indexed by [Understand Anything](https://github.com/Lum1104/Understand-Anything) — a multi-agent pipeline that builds a knowledge graph of every file, function, class, and dependency.

The graph lives at `.understand-anything/knowledge-graph.json` and can be explored visually:

```bash
# In Claude Code, from this repo root:
/understand-dashboard
```

To rebuild the graph after major changes:

```bash
~/scripts/graphify-all.sh
```

> Graph covers: files · functions · classes · imports · architecture layers · plain-English summaries · guided tours.
