# hooks/pre_implementation.md

## Pre-Flight Alignment

1. **Consistency Check:** Cross-reference `SCHEMA_MAPPING.json` with `TEST_TRUTHS.json`. Ensure the "Primary Key" (SKU) is present in both canonical and snapshot mapping.
2. **File Sampling:** Perform a `head -n 5` on both `snapshot_1.csv` and `snapshot_2.csv`.
   - **Validation:** Confirm headers in the files match the "snapshot_2_mapping" keys exactly.
   - **Failure:** If headers do not match, **stop** and ask for a mapping update before writing any code.
3. **Logic Confirmation:**
   - Verify how "quantity" should be handled (Integer vs Float) based on `BUSINESS_CONTEXT.md`.
   - Confirm the "Conflict" definition matches the logic in `TEST_TRUTHS.json`.

## Implementation Strategy

- Plan the code structure using **Modular Functions** (e.g., `load_data`, `apply_mapping`, `reconcile`, `generate_report`).
- **Token Saver:** Do not write the full script yet. Present the function signatures and the plan for confirmation first.
