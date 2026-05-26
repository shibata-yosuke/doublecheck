# doublecheck

`doublecheck` is a local Codex CLI plugin bundle for reviewing a survey preview URL against an Excel questionnaire workbook.

## Repository layout

- [plugin/doublecheck](C:/Users/yamat/Documents/doublecheck/plugin/doublecheck): distributable plugin bundle
- [scripts/upsert_marketplace.py](C:/Users/yamat/Documents/doublecheck/scripts/upsert_marketplace.py): shared installer helper for personal marketplace registration
- [tests](C:/Users/yamat/Documents/doublecheck/tests): unit tests for deterministic helpers
- [install-doublecheck.ps1](C:/Users/yamat/Documents/doublecheck/install-doublecheck.ps1): Windows installer
- [install-doublecheck.sh](C:/Users/yamat/Documents/doublecheck/install-doublecheck.sh): macOS installer

## What the plugin does

The plugin is designed to support this workflow:

1. Validate `doublecheck <preview-url> <excel-file>`.
2. Read the questionnaire workbook through an Excel MCP server.
3. Open the preview page through a Playwright MCP server.
4. Review the survey against the agreed double-check criteria.
5. Emit a Markdown report named `doublecheck_YYYY_MM_DD_HHmm.md`.

## Test command

```powershell
C:\Users\yamat\AppData\Local\Programs\Python\Python313\python.exe -m pytest tests -q
```

## Plugin validation

```powershell
C:\Users\yamat\AppData\Local\Programs\Python\Python313\python.exe C:\Users\yamat\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py C:\Users\yamat\Documents\doublecheck\plugin\doublecheck
```

## Install

Windows:

```powershell
.\install-doublecheck.ps1
```

macOS:

```sh
./install-doublecheck.sh
```
