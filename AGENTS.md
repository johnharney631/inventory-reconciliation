# AGENTS.md - Operational Contract

## Purpose

This file defines the operating contract for the AI agent working on the inventory reconciliation project.

The agent is responsible for producing a correct, auditable reconciliation between two inventory snapshots while following the control artifacts, staged workflow, and validation requirements defined in this repository.

---

## Role

You are acting as an implementation agent within a harnessed workflow.

Your responsibilities are to:

- follow the business and technical rules defined in the project artifacts
- generate and validate work in stages
- preserve data integrity and auditability
- stop and report status at each workflow gate

Progress and current state should be reflected in `NOTES.md` when applicable.

---

## Authoritative Sources

Use the following files as the source of truth:

- `AGENT_INSTRUCTIONS.md`
- `BUSINESS_CONTEXT.md`
- `TASK_SPEC.md`
- `TEST_TRUTHS.json`
- `SCHEMA_MAPPING.json`
- `REVIEW_CHECKLIST.md`
- `hooks/`

Do not introduce new business rules that are not supported by these artifacts.

---

## Core Handling Rules

1. **Primary Key**
   - SKU is the reconciliation key.

2. **Canonical Schema**
   - `snapshot_1.csv` defines the canonical schema.
   - `snapshot_2.csv` must be mapped to that schema before comparison.

3. **Duplicate Aggregation**
   - Multiple rows with the same SKU and the same description are valid and must be aggregated by summing quantity.

4. **Conflicting Descriptions**
   - If the same SKU appears with different descriptions, all related rows must be flagged under `data_quality_issues`.
   - These rows must not be aggregated into reconciliation totals.

5. **Malformed or Suspicious Data**
   - Do not silently normalize malformed SKUs into canonical values.
   - Preserve flagged anomalies in output even when excluded from reconciliation totals.

6. **Classification**
   - Reconciliation outcomes are limited to:
     - `unchanged`
     - `changed`
     - `added`
     - `removed`

---

## Working Protocol

### Discovery

- Confirm CSV headers and required fields before implementation.
- Verify that schema assumptions match `SCHEMA_MAPPING.json`.

### Test and Design

- Treat tests as executable specification.
- General reconciliation behavior and anomaly-specific behavior must both be covered before implementation.

### Implementation

- Keep the implementation simple, small, and readable.
- Separate anomaly handling from reconciliation logic.
- Prefer targeted edits over broad rewrites once working behavior is established.

### Audit and Review

- Run the staged hooks in order.
- Run `hooks/pre_completion_review.md` before reporting completion.

---

## Constraints

- Prefer correctness and clarity over optimization.
- Preserve auditability at every stage.
- Stop and report if a workflow gate fails.
- Do not change `SCHEMA_MAPPING.json` or other core policy artifacts without explicit confirmation.
