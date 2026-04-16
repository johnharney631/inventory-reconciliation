# REVIEW_CHECKLIST.md - Final Quality Gate

## 1. Structural Integrity

- [ ] **Schema:** Does every key in `reconciliation_report.json` match the naming convention in `SCHEMA_MAPPING.json`?
- [ ] **JSON Format:** Is the output a valid JSON object? (No trailing commas or truncated blocks).

## 2. Logic Accuracy

- [ ] **Aggregation:** Are there zero instances of duplicate SKUs in the `unchanged` or `changed` arrays?
- [ ] **Conflict Handling:** Are SKUs with conflicting descriptions moved to `data_quality_issues` and **removed** from reconciliation totals?
- [ ] **Classification:** Is every row from `snapshot_2` accounted for in one of the 5 categories?

## 3. Mathematical Checksum

- [ ] **Total Row Count:** (Unchanged + Changed + Removed) == Total rows in `snapshot_1.csv`?
- [ ] **Anomaly Count:** Does the count of `data_quality_issues` match the number of rows flagged by `TEST_TRUTHS.json`?

## 4. Test Coverage

- [ ] **Anomalies:** Did the test suite successfully trigger and catch a "negative quantity" and a "schema mismatch"?
- [ ] **Pass State:** Did `npm test` return a 0 exit code?
