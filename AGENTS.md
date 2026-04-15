# AGENTS.md

Defines the operating contract for the AI agent.

Inputs:
- BUSINESS_CONTEXT.md
- TASK_SPEC.md
- TEST_TRUTHS.json
- SCHEMA_MAPPING.json
- REVIEW_CHECKLIST.md

Rules:
- SKU is the primary key
- Snapshot 1 is canonical
- Aggregate duplicate rows (same SKU + description)
- Flag and exclude conflicting descriptions
- Separate anomaly handling from reconciliation

Execution:
Follow the staged workflow defined in AGENT_INSTRUCTIONS.md

Completion:
- All tests pass
- Output matches required JSON structure
- REVIEW_CHECKLIST.md is satisfied
