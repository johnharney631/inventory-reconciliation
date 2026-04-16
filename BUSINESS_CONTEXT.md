# BUSINESS_CONTEXT.md

- **Project:** Inventory Reconciliation (POC)
- **Goal:** Identify discrepancies between Source of Truth (Snapshot 1) and Warehouse Export (Snapshot 2).
- **Critical Success Factor:** Zero loss of SKU data; all anomalies must be accounted for in the final JSON.
- **Priority:** Accuracy over speed. If data is ambiguous, flag as an anomaly.
