# TASK_SPEC.md

Defines the task requirements.

Inputs:
- snapshot_1.csv (canonical)
- snapshot_2.csv (mapped)

Outputs:
- JSON report with:
  - unchanged
  - changed
  - added
  - removed
  - data_quality_issues (grouped)

Rules:
- Aggregate valid duplicates
- Flag conflicting descriptions
- Apply schema mapping before comparison
