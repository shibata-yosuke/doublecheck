# Doublecheck Plugin Design

## Goal

Create a Codex CLI local plugin named `doublecheck` that automates questionnaire preview double-checks by combining:

- Excel questionnaire reading through an Excel MCP server
- Preview page inspection through a Playwright MCP server
- AI-driven review output in the Codex CLI conversation and a saved Markdown report

The plugin must be distributable to local user environments on Windows 11 and macOS through one-click install scripts.

## Scope

This design covers:

- Local Codex CLI plugin structure
- Invocation model for `doublecheck <preview-url> <excel-file>`
- MCP packaging and registration inside the plugin
- Validation and reporting flow
- Windows and macOS distribution scripts

This design does not cover:

- Building a custom Excel MCP server
- Building a custom Playwright MCP server
- Remote/cloud deployment
- A GUI outside Codex CLI

## User Workflow

1. The user runs the provided install script on Windows 11 or macOS.
2. The script installs the plugin into the user's personal local Codex plugin area:
   - plugin source under `~/plugins/doublecheck`
   - marketplace registration in `~/.agents/plugins/marketplace.json`
3. The script places or configures the plugin-local MCP definitions required for Excel and Playwright access.
4. The user opens Codex CLI in a folder containing the target `.xlsx` questionnaire file.
5. The user invokes `doublecheck` and provides:
   - a Freeasy preview URL
   - a questionnaire Excel filename
6. The plugin validates the inputs and required local runtime conditions.
7. If validation fails, the plugin exits immediately with a concrete reason.
8. If validation succeeds:
   - the Excel MCP server reads the questionnaire workbook
   - the Playwright MCP server opens the preview URL
   - the plugin guides Codex to review the survey against the approved double-check criteria
9. Codex outputs:
   - a short conversation summary
   - a Markdown report file named `doublecheck_YYYY_MM_DD_HHmm.md`

## Review Criteria

The plugin workflow must support review against the following criteria from the source spec:

- Wording is easy for respondents to understand quickly.
- Wording does not create multiple plausible interpretations.
- Similar question and choice wording is normalized consistently.
- Scale direction is natural and consistent across questions.
- Skip logic and transitions do not force inapplicable answers.
- Ordered choices are not randomized when order has meaning.
- Brand or item names and images are correct and commonly recognizable.
- Images are sufficiently legible.
- Text inside images is readable.
- Single-choice, multi-choice, matrix, branch conditions, and display conditions are correctly designed.
- Randomization is enabled where appropriate without causing confusion.
- Question order and choice order do not introduce unintended bias.
- Options are MECE where expected.
- Numeric or range options are realistic and properly bounded.
- Targeting conditions match agreed respondent criteria.
- Pre/Post studies are aligned for valid comparison.
- Media-contact questions match the media plan when applicable.

## Recommended Architecture

### Plugin name and location

- Plugin name: `doublecheck`
- Personal plugin location: `~/plugins/doublecheck`
- Personal marketplace file: `~/.agents/plugins/marketplace.json`

### Plugin contents

The plugin should contain:

- `.codex-plugin/plugin.json`
- `.mcp.json`
- `skills/doublecheck/SKILL.md`
- `scripts/`
- optional `README.md` for local maintainers

### Responsibility split

`plugin.json`
- Defines plugin identity and enabled components.

`.mcp.json`
- Declares the Excel MCP server and Playwright MCP server used by this plugin.

`skills/doublecheck/SKILL.md`
- Defines the user-facing entrypoint behavior.
- Documents the expected command form, preconditions, review criteria, and output behavior.

`scripts/`
- Handles deterministic helper logic only.
- Intended uses:
  - input validation
  - report filename generation
  - Markdown report formatting
  - normalization of collected findings into a stable structure

The plugin must not reimplement Excel reading or browser automation that existing MCP servers already handle well.

## Execution Flow

### Command contract

Primary command shape:

```text
doublecheck <preview-url> <excel-file>
```

Expected examples:

```text
doublecheck https://monitor.research-plus.net/enquete_preview_list/?e=... questionnaire.xlsx
```

### Preconditions

Before analysis begins, the plugin must verify:

- the preview URL is syntactically valid
- the Excel file exists in the current working directory or provided path
- the file extension is `.xlsx`
- required MCP definitions are present
- required runtimes for configured MCP servers are available

### Failure behavior

The plugin must fail fast and stop when:

- URL format is invalid
- Excel file is missing
- file extension is unsupported
- Excel MCP server cannot start
- Playwright MCP server cannot start
- preview page cannot be opened
- workbook cannot be read

Failures should be reported with explicit, user-readable reasons. The plugin should not continue in degraded mode when core inputs cannot be inspected.

### Analysis behavior

On success, the plugin flow is:

1. Read questionnaire structure and relevant contents through the Excel MCP server.
2. Open the preview page through the Playwright MCP server.
3. Inspect survey pages, options, branches, scales, images, and wording.
4. Compare questionnaire structure and preview behavior against the review criteria.
5. Normalize findings into a stable report structure.
6. Present a concise conversation summary.
7. Persist a Markdown report in the current working directory.

## Output Specification

### CLI conversation output

The conversation summary should be concise and include:

- total issue count
- high-severity issue count if any
- major correction candidates
- whether some checks were not possible

### Markdown report output

Filename format:

```text
doublecheck_YYYY_MM_DD_HHmm.md
```

The report should include:

- execution timestamp
- input preview URL
- input Excel filename
- summary of results
- findings grouped by criterion or severity
- affected question/page/choice references when identifiable
- recommended fixes
- unchecked or inconclusive items marked explicitly as unverified

The report must be written even when the result is "no issues found," as long as execution completed normally.

## Distribution Design

### Windows 11 installer

Provide `install-doublecheck.ps1`.

Responsibilities:

- create the target plugin directory if absent
- copy plugin files into `~/plugins/doublecheck`
- create or update `~/.agents/plugins/marketplace.json`
- preserve existing marketplace metadata where possible
- append the plugin entry if not present
- be safe to rerun without corrupting the plugin installation

### macOS installer

Provide `install-doublecheck.sh`.

Responsibilities are the same as the PowerShell installer:

- create the target plugin directory if absent
- copy plugin files into `~/plugins/doublecheck`
- create or update `~/.agents/plugins/marketplace.json`
- preserve existing marketplace metadata where possible
- append the plugin entry if not present
- be safe to rerun

### Marketplace entry

The plugin should be registered as a personal local plugin using the standard local marketplace structure, with `source.path` set to `./plugins/doublecheck`.

## Validation Strategy

Validation should cover three layers:

### 1. Helper script validation

Confirm deterministic helpers behave correctly:

- argument validation
- report naming
- Markdown emission

### 2. Plugin integration validation

Confirm Codex CLI recognizes the plugin and the `doublecheck` skill entrypoint.

### 3. End-to-end workflow validation

Confirm:

- a valid sample Excel file and preview URL run successfully
- invalid URL fails early
- missing Excel file fails early
- output report file is created on success

## Design Constraints

- Favor reuse of existing MCP servers over building custom equivalents.
- Keep AI-specific judgment in the skill flow, not hardcoded into deterministic scripts.
- Keep deterministic tasks in local scripts so outputs are stable and testable.
- Do not silently skip core checks when required tooling fails.
- Treat "unable to verify" as a first-class output state rather than pretending success.

## Open Implementation Decisions

These are implementation-level details, not blockers to this design:

- exact MCP server packaging method inside the distributed plugin bundle
- exact script language split inside `scripts/` between Python and shell
- exact internal report schema before Markdown rendering

The implementation should choose the simplest approach that keeps both installers rerunnable and the plugin maintainable.
