---
description: Search the pattern library and codebase before writing new code
argument-hint: [what you're about to build]
allowed-tools: [Read, Bash, Grep, Glob]
---

Pattern-first: find something to reuse before creating.

```bash
cat patterns_library/README.md 2>/dev/null
ls patterns_library/ 2>/dev/null
grep -ri "$1" patterns_library/ specs/ 2>/dev/null | head
```

Also scan existing ontologies / code for similar shapes. Report:

- **matching patterns** → reuse these,
- **near-misses** → adapt,
- **none** → propose a new pattern to the System Architect.

Do not implement until a pattern is chosen or approved.
