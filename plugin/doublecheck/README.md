# Doublecheck Plugin Bundle

This directory is the distributable Codex CLI plugin bundle for `doublecheck`.

## Contents

- `.codex-plugin/plugin.json`: plugin manifest
- `.mcp.json`: Excel and Playwright MCP server definitions
- `skills/doublecheck/SKILL.md`: user-facing workflow entrypoint
- `scripts/`: deterministic helpers for validation and report generation

## MCP choices

- Excel MCP: `@negokaz/excel-mcp-server`
- Playwright MCP: `@playwright/mcp`

These are fetched through `npx` so the installer only needs a working Node.js/npm setup.
