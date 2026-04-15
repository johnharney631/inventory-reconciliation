import json
import os
import re

import pandas as pd

CANONICAL_SKU = re.compile(r"^SKU-\d+$")


def map_snapshot2_columns(df):
    return df.rename(columns={
        "product_name": "name",
        "qty": "quantity",
        "warehouse": "location",
        "updated_at": "last_counted",
    })


def reconcile(df1, df2):
    df1 = df1.copy()
    df2 = df2.copy()

    # Normalize whitespace in string fields
    for df in (df1, df2):
        df["sku"] = df["sku"].str.strip()
        df["name"] = df["name"].str.strip()

    # Ensure quantity is numeric
    df1["quantity"] = pd.to_numeric(df1["quantity"], errors="coerce")
    df2["quantity"] = pd.to_numeric(df2["quantity"], errors="coerce")

    issues = {
        "conflicting_descriptions_for_sku": [],
        "duplicate_rows_same_description": [],
        "invalid_quantity": [],
        "formatting_issues": [],
        "schema_mismatch": [],
    }

    excluded_skus = set()

    # Flag malformed SKUs in snapshot_2 (flagged but not excluded)
    for _, row in df2[~df2["sku"].str.match(CANONICAL_SKU)].iterrows():
        issues["schema_mismatch"].append(row.to_dict())

    # Detect conflicting descriptions in each snapshot before any row removal
    # so that rows with both a conflict and invalid qty are caught by both checks
    for df in (df1, df2):
        for sku, group in df.groupby("sku"):
            if group["name"].nunique() > 1:
                excluded_skus.add(sku)
                for _, row in group.iterrows():
                    issues["conflicting_descriptions_for_sku"].append(row.to_dict())

    # Detect invalid quantities in both snapshots
    for df in (df1, df2):
        for _, row in df[df["quantity"] < 0].iterrows():
            excluded_skus.add(row["sku"])
            issues["invalid_quantity"].append(row.to_dict())

    # Remove all excluded SKUs from the working sets
    w1 = df1[~df1["sku"].isin(excluded_skus)]
    w2 = df2[~df2["sku"].isin(excluded_skus)]

    # Flag duplicate rows (same SKU + same name) for audit
    for df in (w1, w2):
        for _, group in df.groupby("sku"):
            if len(group) > 1:
                for _, row in group.iterrows():
                    issues["duplicate_rows_same_description"].append(row.to_dict())

    # Aggregate valid duplicate rows by summing quantities
    def aggregate(df):
        if df.empty:
            return df
        return df.groupby("sku", as_index=False).agg(
            name=("name", "first"),
            quantity=("quantity", "sum"),
            location=("location", "first"),
            last_counted=("last_counted", "first"),
        )

    a1 = aggregate(w1)
    a2 = aggregate(w2)

    # Merge and classify
    merged = a1.merge(a2, on="sku", how="outer", suffixes=("_1", "_2"))

    unchanged, changed, added, removed = [], [], [], []

    for _, row in merged.iterrows():
        sku = row["sku"]
        in_s1 = pd.notna(row.get("quantity_1"))
        in_s2 = pd.notna(row.get("quantity_2"))

        if in_s1 and in_s2:
            q1 = int(row["quantity_1"])
            q2 = int(row["quantity_2"])
            name = row["name_1"]
            if q1 == q2:
                unchanged.append({"sku": sku, "name": name, "quantity": q1})
            else:
                changed.append({
                    "sku": sku,
                    "name": name,
                    "quantity_snapshot_1": q1,
                    "quantity_snapshot_2": q2,
                })
        elif in_s2:
            added.append({"sku": sku, "name": row["name_2"], "quantity": int(row["quantity_2"])})
        else:
            removed.append({"sku": sku, "name": row["name_1"], "quantity": int(row["quantity_1"])})

    return {
        "summary": {
            "unchanged": len(unchanged),
            "changed": len(changed),
            "added": len(added),
            "removed": len(removed),
            "data_quality_issues": sum(len(v) for v in issues.values()),
        },
        "unchanged": unchanged,
        "changed": changed,
        "added": added,
        "removed": removed,
        "data_quality_issues": issues,
    }


def main():
    s1_path = "data/snapshot_1.csv"
    s2_path = "data/snapshot_2.csv"
    output_path = "output/reconciliation_report.json"

    df1 = pd.read_csv(s1_path)
    df2 = map_snapshot2_columns(pd.read_csv(s2_path))

    report = reconcile(df1, df2)

    os.makedirs("output", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report written to {output_path}")
    print(f"Summary: {report['summary']}")


if __name__ == "__main__":
    main()
