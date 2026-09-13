---
name: pattern-discovery
description: Search first, reuse always — check the pattern library and existing work before writing anything new. Use before implementing any feature, ontology shape, or mapping.
---

# Pattern discovery

Search before you build. Reuse beats reinvention and keeps the system coherent.

## Look, in order

```bash
cat patterns_library/README.md   # existing patterns
ls decisions/                    # settled decisions — do not relitigate
ls specs/                        # related initiatives
grep -ri "<what you're building>" patterns_library/ specs/
```

Also scan existing ontologies / code for similar shapes.

## Decide

- **Match** → reuse it.
- **Near-miss** → adapt it.
- **None** → propose a new pattern to the System Architect (who approves it into `patterns_library/`).

Do not implement until a pattern is chosen or approved. Divergent one-offs are how systems rot.
