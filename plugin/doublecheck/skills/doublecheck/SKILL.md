---
name: doublecheck
description: Review a Freeasy preview URL against an Excel questionnaire workbook and emit a Markdown report with issues, risks, and unverified checks.
---

# Doublecheck

Use this skill when the user wants to review a survey preview against its questionnaire workbook.

## Input contract

Expected invocation shape:

```text
doublecheck <preview-url> <excel-file>
```

Example:

```text
doublecheck https://monitor.research-plus.net/enquete_preview_list/?e=... questionnaire.xlsx
```

## Preconditions

Before starting the review:

1. Validate the preview URL with `scripts/doublecheck_args.py`.
2. Validate that the Excel file exists and ends in `.xlsx`.
3. Confirm the `excel` and `playwright` MCP servers are available from `.mcp.json`.

If any precondition fails, stop immediately and explain the exact reason.

## Workflow

1. Read the questionnaire workbook through the `excel` MCP server.
2. Open the preview URL through the `playwright` MCP server.
3. Compare workbook structure and preview behavior.
4. Review against these criteria:
   - easy-to-understand wording
   - no ambiguous expressions
   - consistent wording across related items
   - natural and consistent scale direction
   - correct skip logic and transitions
   - no invalid randomization on ordered choices
   - correct and recognizable brand names and images
   - readable images and readable text inside images
   - correct answer type, matrix, branch, and display-condition design
   - appropriate randomization where useful
   - no unintended order bias
   - MECE choice sets where expected
   - realistic numeric and range choices
   - targeting criteria aligned with the agreed respondent definition
   - pre/post comparability where applicable
   - media-plan alignment where applicable
5. Summarize findings in the conversation.
6. Save a Markdown report through `scripts/doublecheck_report.py`.

## Output contract

- Always emit a short summary in the conversation.
- On successful execution, always write a report named `doublecheck_YYYY_MM_DD_HHmm.md`.
- Mark checks as `unverified` when the information was not available instead of assuming success.
