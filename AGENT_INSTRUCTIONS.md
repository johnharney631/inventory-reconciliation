# AGENT_INSTRUCTIONS.md - Execution Entry Point

## Purpose

This file defines how the AI agent should execute the inventory reconciliation project within the harnessed workflow.

The agent must follow the control artifacts, complete work in stages, and stop after each stage for review before proceeding.

---

## Entry Protocol

1. Read `AGENTS.md` to understand operating rules, workflow, and completion criteria.
2. Confirm the presence of the required project files:
   - `BUSINESS_CONTEXT.md`
   - `TASK_SPEC.md`
   - `TEST_TRUTHS.json`
   - `SCHEMA_MAPPING.json`
   - `REVIEW_CHECKLIST.md`
   - `data/snapshot_1.csv`
   - `data/snapshot_2.csv`
3. Check `NOTES.md` for prior progress and resume from the last completed stage if applicable.

---

## Staged Workflow

Execute the following in strict order.  
After each stage, stop and report status before continuing.

### Phase 1: Alignment

Run `hooks/pre_implementation.md`

Goals:

- confirm project intent
- confirm canonical schema assumptions
- confirm required rules before implementation

### Phase 2: Design and Test

Run `hooks/pre_test_generation.md`

Goals:

- generate tests before implementation
- cover both general reconciliation behavior and anomaly-specific cases
- treat tests as executable specification

### Phase 3: Implementation

Implement the reconciliation logic.

Requirements:

- keep the implementation simple, clear, and modular
- do not over-engineer
- do not silently normalize malformed SKUs into canonical values
- preserve flagged anomalies in output even when excluded from reconciliation totals
- do not introduce business rules not defined in the control artifacts

### Phase 4: Output Validation

Run `hooks/pre_output_validation.md`

Goals:

- validate JSON structure
- confirm grouped issue reporting
- confirm reconciliation totals and classifications are consistent

### Phase 5: Completion Review

Run `hooks/pre_completion_review.md`

Goals:

- validate against `REVIEW_CHECKLIST.md`
- confirm all tests pass
- confirm `NOTES.md` remains aligned with implementation behavior

---

## Error Handling

- If a hook fails, stop immediately.
- Summarize the failure and propose the smallest reasonable fix.
- Do not change `SCHEMA_MAPPING.json` or any core policy artifact without explicit confirmation.
- Do not proceed past a failed stage.

---

## Operating Constraints

- Prefer clarity and correctness over optimization.
- Keep the Python implementation small; complexity belongs in the harness, not the script.
- Separate anomaly handling from reconciliation logic.
- Preserve auditability at every stage.
