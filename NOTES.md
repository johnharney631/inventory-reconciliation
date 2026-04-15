# NOTES.md

## Key Decisions / Assumptions

**Overall**  
The project is structured to demonstrate **AI-forward / harness engineering** by separating business context, specifications, workflow control, and validation from implementation.

Control artifacts included:

- BUSINESS_CONTEXT.md
- TASK_SPEC.md
- TEST_TRUTHS.json
- SCHEMA_MAPPING.json
- REVIEW_CHECKLIST.md
- hooks/pre_implementation.md
- hooks/pre_test_generation.md
- hooks/pre_output_validation.md
- hooks/pre_completion_review.md

**Architectural**

- **SKU as primary key** with snapshot 1 as the canonical schema; snapshot 2 is mapped to it
- **Duplicate rows (same SKU + description)** are aggregated by summing quantities since a product can exist in multiple bins/locations
- **Conflicting descriptions for a SKU** are treated as invalid; all rows are flagged and excluded from totals
- **Schema differences** are handled via explicit column mapping
- **Reconciliation** is performed on normalized, aggregated data (not row-level)

---

## Data Quality Issues Observed

- **Conflicting descriptions for the same SKU** (excluded from totals)
- **Duplicate rows with consistent data** (aggregated)
- **Invalid quantities** (e.g., negative values)
- **Formatting inconsistencies** (whitespace, casing)
- **Schema inconsistencies** (column name mismatches)

Issues are surfaced separately to preserve auditability and avoid masking data integrity problems.

---

## Approach

1. Normalize both datasets into a canonical schema
2. Identify and isolate data quality issues early
3. Aggregate valid data at the SKU level
4. Reconcile based on presence and total quantity
5. Output a structured JSON report including results and data quality findings

This approach ensures reconciliation is accurate, explainable, and robust to real-world data issues.

---

## Tooling Decisions

**Testing framework: pytest**
Chosen for its concise syntax, powerful fixture system, and better readability of failure output compared to unittest. No project constraint required stdlib-only.

**Data library: pandas**
Chosen for its first-class CSV handling, vectorized operations, and straightforward groupby/merge semantics that map cleanly to reconciliation logic. The README explicitly allowed any helpful libraries.

---

## Schema Decisions

**Snapshot 1 column names are canonical**
The reconciliation uses snapshot 1's column names (`sku`, `name`, `quantity`) as the standard. Snapshot 2's columns (`sku`, `product_name`, `qty`) are mapped to match. Columns not relevant to reconciliation (`location`, `last_counted` from snapshot 1; `warehouse`, `updated_at` from snapshot 2) are excluded.

**SKU formatting anomalies in snapshot 2 are flagged, not normalized**
SKUs like `SKU005`, `sku-008`, and `SKU018` that don't match the canonical `SKU-###` format are treated as data quality issues and excluded from reconciliation rather than silently corrected.
