# hooks/pre_output_validation.md

## Data Integrity Audit

1. **Category Coverage:** Verify the JSON contains all 6 required keys.
2. **Mathematical Checksum:**
   - Total Source Rows = Count(unchanged) + Count(changed) + Count(removed).
   - If the numbers do not add up, **STOP**. Re-scan the source file to find the "dropped" rows.
3. **Anomaly Grouping:**
   - Ensure `data_quality_issues` are grouped by the `anomaly_types` defined in `TEST_TRUTHS.json`.
   - Verify that any SKU in the "issues" group is **EXCLUDED** from the "changed/unchanged" totals to prevent double-counting.
4. **Schema Integrity:**
   - Confirm all keys in the `changed` objects use the **canonical** names from `SCHEMA_MAPPING.json`, not the raw snapshot headers.

## Output Efficiency

- If the report lists more than 100 rows per category, save the full JSON to a file (e.g., `final_report.json`) and only display a **summary table** in the chat.
- _Why:_ Sending 5,000 lines of JSON to the terminal is the fastest way to hit your session limit.
