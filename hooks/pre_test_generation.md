# hooks/pre_test_generation.md

## Test Design Specifications

1. **Mock Data Creation:** Generate a `test_source.csv` and `test_target.csv` with exactly ONE representative case for:
   - `unchanged`: Identical data.
   - `changed`: Same SKU, different quantity.
   - `added`: SKU only in target.
   - `removed`: SKU only in source.
2. **Anomaly Injection:** Intentionally include:
   - One "Conflicting Description" (Same SKU, different string).
   - One "Invalid Quantity" (Negative or non-numeric).
3. **Assertion Logic:**
   - Write a test script (e.g., `test_reconciliation.py/ts`) that asserts the final JSON counts match your mock data exactly.
   - Ensure the test checks that "Conflicting Descriptions" are **successfully excluded** from the main totals.

## Verification

- Run the test suite. It **must fail** (Red phase) because the implementation doesn't exist yet.
- Only once the tests are confirmed to fail correctly, proceed to Phase 3 of `AGENT_INSTRUCTIONS.md`.
