# Doublecheck Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local Codex CLI plugin named `doublecheck` plus Windows and macOS installers that register the plugin in the personal marketplace and support questionnaire preview double-check workflows.

**Architecture:** Keep the plugin thin. The skill defines the review workflow, Python helpers handle deterministic validation and Markdown rendering, and plugin-local MCP definitions point at Excel and Playwright capabilities. Installers copy the plugin bundle into the standard personal plugin path and upsert the marketplace entry idempotently.

**Tech Stack:** Codex plugin manifest JSON, plugin skill markdown, Python 3.13 helpers, PowerShell, POSIX shell

---

### Task 1: Scaffold the plugin bundle and manifests

**Files:**
- Create: `plugin/doublecheck/.codex-plugin/plugin.json`
- Create: `plugin/doublecheck/.mcp.json`
- Create: `plugin/doublecheck/README.md`
- Create: `plugin/doublecheck/skills/doublecheck/SKILL.md`

- [ ] Create the plugin directory structure with the required manifest files.
- [ ] Fill `plugin.json` with a validation-safe manifest that exposes `skills/` and `.mcp.json`.
- [ ] Define the skill entrypoint contract in `skills/doublecheck/SKILL.md`.
- [ ] Add placeholder-but-valid local MCP entries in `.mcp.json` for Excel and Playwright.

### Task 2: Build deterministic helper scripts

**Files:**
- Create: `plugin/doublecheck/scripts/doublecheck_args.py`
- Create: `plugin/doublecheck/scripts/doublecheck_report.py`
- Create: `plugin/doublecheck/scripts/sample_findings.json`

- [ ] Write tests first for argument validation behavior and expected failure messages.
- [ ] Implement the minimal validator for URL, `.xlsx` extension, and file existence.
- [ ] Write tests first for report filename generation and Markdown rendering.
- [ ] Implement the report helper so successful runs can always emit `doublecheck_YYYY_MM_DD_HHmm.md`.

### Task 3: Add automated tests for helper scripts

**Files:**
- Create: `tests/test_doublecheck_args.py`
- Create: `tests/test_doublecheck_report.py`

- [ ] Add focused tests for valid and invalid URL handling.
- [ ] Add focused tests for missing files and non-`.xlsx` files.
- [ ] Add focused tests for timestamped report file naming.
- [ ] Add focused tests for Markdown content sections and unverified-item rendering.

### Task 4: Implement installers for Windows and macOS

**Files:**
- Create: `install-doublecheck.ps1`
- Create: `install-doublecheck.sh`

- [ ] Write tests first for marketplace upsert behavior where feasible in Python-backed helper coverage.
- [ ] Implement the PowerShell installer to copy `plugin/doublecheck` into `~/plugins/doublecheck`.
- [ ] Implement the macOS shell installer with the same destination and idempotent marketplace registration.
- [ ] Ensure both installers preserve existing marketplace metadata and only upsert the `doublecheck` entry.

### Task 5: Add shared installer helper logic

**Files:**
- Create: `scripts/upsert_marketplace.py`

- [ ] Add tests first for creating a new marketplace file and updating an existing one.
- [ ] Implement the helper so both installers can reuse the same JSON merge logic.
- [ ] Keep the plugin marketplace entry shape aligned with local plugin requirements.

### Task 6: Validate the bundle and verify locally

**Files:**
- Modify: `README.md`

- [ ] Document the repository layout, test command, and install commands in `README.md`.
- [ ] Run the unit tests for the helper scripts.
- [ ] Run plugin validation against `plugin/doublecheck`.
- [ ] Record any limitations that remain, especially around real MCP server packaging versus local paths.
