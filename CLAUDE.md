# CLAUDE.md

## Purpose

This file provides Claude-specific operating guidance for working in this repository.

The primary workflow contract is defined in:

- `AGENT_INSTRUCTIONS.md`
- `AGENTS.md`

Use this file only as a lightweight execution guide.

## Reference Order

1. `AGENT_INSTRUCTIONS.md`
2. `AGENTS.md`
3. `BUSINESS_CONTEXT.md`
4. `TASK_SPEC.md`
5. `TEST_TRUTHS.json`
6. `SCHEMA_MAPPING.json`
7. `REVIEW_CHECKLIST.md`
8. `hooks/`

## Working Rules

- Read only the files relevant to the current step
- Do not scan the entire repository unless required
- Treat tests as executable specification
- Keep changes minimal and targeted
- Prefer diffs or small edits over full-file rewrites when practical
- Do not invent business rules outside the control artifacts
- Stop after each workflow stage and report status before continuing

## Project Commands

- Run tests: `pytest`
- Run implementation: `python reconcile.py`
