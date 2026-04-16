# TASK_SPEC.md - Data Reconciliation Logic

## Objective

Generate a JSON diff report comparing `snapshot_1.csv` (Source of Truth) against `snapshot_2.csv` (Target).

## Core Pipeline

1. **Load Schema:** Read `SCHEMA_MAPPING.json` first. Do not guess column relationships.
2. **Pre-process:**
   - **Aggregate:** Merge rows with identical IDs. Sum numeric values; join string values with `;`.
   - **Validate:** Group rows that fail `TEST_TRUTHS.json` into `data_quality_issues`.
3. **Comparison Logic:**
   - **Unchanged:** Full field-level match after mapping.
   - **Changed:** ID exists in both, but values differ (flag "Conflicting Descriptions" here).
   - **Added:** ID exists in `snapshot_2` only.
   - **Removed:** ID exists in `snapshot_1` only.

## Output Requirements

- Final file must be `reconciliation_report.json`.
- If `data_quality_issues` exceed 10% of total rows, stop and alert user before proceeding.
