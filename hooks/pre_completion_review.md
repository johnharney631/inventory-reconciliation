# hooks/pre_completion_review.md

## Final Verification Protocol

1. **Test Execution:** Run `npm test` (or equivalent). If any tests fail, **DO NOT** signal completion. Fix the code and restart the hook.
2. **Review Checklist:** Read `REVIEW_CHECKLIST.md`. Explicitly verify that the `reconciliation_report.json` contains all five required categories from `TASK_SPEC.md`.
3. **Internal Consistency:**
   - Verify that `data_quality_issues` includes the specific anomalies defined in `TEST_TRUTHS.json`.
   - Ensure `NOTES.md` accurately reflects any schema deviations encountered during mapping.
4. **Final Checksum:** Confirm that (Unchanged + Changed + Removed) equals the total row count of `snapshot_1.csv`.

## Completion Signal

- Only provide the "Task Complete" summary if **all** points above are validated.
- If checks fail, provide a concise diff of the fix needed—**do not** rewrite entire files.
