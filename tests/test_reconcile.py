import pandas as pd
import pytest

from reconcile import map_snapshot2_columns, reconcile


# --- fixture helpers ---

def s1(*rows):
    """Build a snapshot-1-schema DataFrame from dicts."""
    return pd.DataFrame(rows, columns=["sku", "name", "quantity", "location", "last_counted"])


def s2(*rows):
    """Build an already-mapped (canonical) snapshot-2 DataFrame from dicts."""
    return pd.DataFrame(rows, columns=["sku", "name", "quantity", "location", "last_counted"])


def empty():
    return pd.DataFrame(columns=["sku", "name", "quantity", "location", "last_counted"])


# --- Test 1: schema mapping ---

def test_snapshot2_columns_mapped():
    raw = pd.DataFrame([{
        "sku": "SKU-001",
        "product_name": "Widget A",
        "qty": 10,
        "warehouse": "WH-A",
        "updated_at": "2024-01-15",
    }])
    result = map_snapshot2_columns(raw)
    assert list(result.columns) == ["sku", "name", "quantity", "location", "last_counted"]


# --- Test 2: aggregate same SKU + same name ---

def test_aggregate_same_sku_same_name():
    df1 = s1({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-08"})
    df2 = s2(
        {"sku": "SKU-001", "name": "Widget A", "quantity": 40, "location": "WH-A", "last_counted": "2024-01-15"},
        {"sku": "SKU-001", "name": "Widget A", "quantity": 60, "location": "WH-B", "last_counted": "2024-01-15"},
    )
    report = reconcile(df1, df2)
    assert len(report["unchanged"]) == 1
    assert report["unchanged"][0]["sku"] == "SKU-001"


# --- Test 2b: aggregate same SKU + same name in snapshot 1 ---

def test_aggregate_same_sku_same_name_snapshot1():
    df1 = s1(
        {"sku": "SKU-001", "name": "Widget A", "quantity": 60, "location": "WH-A", "last_counted": "2024-01-08"},
        {"sku": "SKU-001", "name": "Widget A", "quantity": 40, "location": "WH-B", "last_counted": "2024-01-08"},
    )
    df2 = s2({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-15"})
    report = reconcile(df1, df2)
    assert len(report["unchanged"]) == 1
    assert report["unchanged"][0]["sku"] == "SKU-001"


# --- Test 3: conflicting descriptions flagged ---

def test_conflicting_descriptions_flagged():
    df1 = s1({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-08"})
    df2 = s2(
        {"sku": "SKU-001", "name": "Widget A",     "quantity": 50, "location": "WH-A", "last_counted": "2024-01-15"},
        {"sku": "SKU-001", "name": "Widget Alpha",  "quantity": 50, "location": "WH-A", "last_counted": "2024-01-15"},
    )
    report = reconcile(df1, df2)
    conflicts = report["data_quality_issues"]["conflicting_descriptions_for_sku"]
    assert len(conflicts) == 2
    assert all(r["sku"] == "SKU-001" for r in conflicts)


# --- Test 3b: conflicting descriptions in snapshot 1 flagged and excluded ---

def test_conflicting_descriptions_flagged_snapshot1():
    df1 = s1(
        {"sku": "SKU-001", "name": "Widget A",    "quantity": 50, "location": "WH-A", "last_counted": "2024-01-08"},
        {"sku": "SKU-001", "name": "Widget Alpha", "quantity": 50, "location": "WH-B", "last_counted": "2024-01-08"},
    )
    df2 = s2({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-15"})
    report = reconcile(df1, df2)
    conflicts = report["data_quality_issues"]["conflicting_descriptions_for_sku"]
    assert len(conflicts) == 2
    assert all(r["sku"] == "SKU-001" for r in conflicts)
    all_skus = (
        [r["sku"] for r in report["unchanged"]]
        + [r["sku"] for r in report["changed"]]
        + [r["sku"] for r in report["added"]]
        + [r["sku"] for r in report["removed"]]
    )
    assert "SKU-001" not in all_skus


# --- Test 4: conflicting descriptions excluded from reconciliation totals ---

def test_conflicting_descriptions_excluded_from_totals():
    df1 = s1({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-08"})
    df2 = s2(
        {"sku": "SKU-001", "name": "Widget A",    "quantity": 50, "location": "WH-A", "last_counted": "2024-01-15"},
        {"sku": "SKU-001", "name": "Widget Alpha", "quantity": 50, "location": "WH-A", "last_counted": "2024-01-15"},
    )
    report = reconcile(df1, df2)
    all_skus = (
        [r["sku"] for r in report["unchanged"]]
        + [r["sku"] for r in report["changed"]]
        + [r["sku"] for r in report["added"]]
        + [r["sku"] for r in report["removed"]]
    )
    assert "SKU-001" not in all_skus


# --- Test 5: unchanged ---

def test_unchanged():
    df1 = s1({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-08"})
    df2 = s2({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-15"})
    report = reconcile(df1, df2)
    assert len(report["unchanged"]) == 1
    assert report["unchanged"][0]["sku"] == "SKU-001"


# --- Test 6: changed ---

def test_changed():
    df1 = s1({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-08"})
    df2 = s2({"sku": "SKU-001", "name": "Widget A", "quantity": 90,  "location": "WH-A", "last_counted": "2024-01-15"})
    report = reconcile(df1, df2)
    assert len(report["changed"]) == 1
    row = report["changed"][0]
    assert row["sku"] == "SKU-001"
    assert row["quantity_snapshot_1"] == 100
    assert row["quantity_snapshot_2"] == 90


# --- Test 7: added ---

def test_added():
    df2 = s2({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-15"})
    report = reconcile(empty(), df2)
    assert len(report["added"]) == 1
    assert report["added"][0]["sku"] == "SKU-001"


# --- Test 8: removed ---

def test_removed():
    df1 = s1({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-08"})
    report = reconcile(df1, empty())
    assert len(report["removed"]) == 1
    assert report["removed"][0]["sku"] == "SKU-001"


# --- Test 9: invalid quantity flagged and excluded from reconciliation ---

def test_invalid_quantity_flagged():
    df1 = s1({"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-08"})
    df2 = s2({"sku": "SKU-001", "name": "Widget A", "quantity": -5,  "location": "WH-A", "last_counted": "2024-01-15"})
    report = reconcile(df1, df2)
    invalid = report["data_quality_issues"]["invalid_quantity"]
    assert len(invalid) == 1
    assert invalid[0]["sku"] == "SKU-001"
    all_skus = (
        [r["sku"] for r in report["unchanged"]]
        + [r["sku"] for r in report["changed"]]
        + [r["sku"] for r in report["added"]]
        + [r["sku"] for r in report["removed"]]
    )
    assert "SKU-001" not in all_skus


# --- Test 10: conflict + invalid quantity both flagged (SKU-045 scenario) ---

def test_invalid_quantity_and_conflict_both_flagged():
    df1 = s1({"sku": "SKU-045", "name": "Multimeter Pro", "quantity": 25, "location": "WH-A", "last_counted": "2024-01-08"})
    df2 = s2(
        {"sku": "SKU-045", "name": "Multimeter Professional", "quantity": 23, "location": "WH-A", "last_counted": "2024-01-15"},
        {"sku": "SKU-045", "name": "Multimeter Pro",          "quantity": -5, "location": "WH-B", "last_counted": "2024-01-15"},
    )
    report = reconcile(df1, df2)
    conflict_skus = [r["sku"] for r in report["data_quality_issues"]["conflicting_descriptions_for_sku"]]
    invalid_skus  = [r["sku"] for r in report["data_quality_issues"]["invalid_quantity"]]
    assert "SKU-045" in conflict_skus
    assert "SKU-045" in invalid_skus


# --- Test 11: malformed SKU flagged ---

def test_malformed_sku_flagged():
    df2 = s2({"sku": "SKU005", "name": "Widget A", "quantity": 10, "location": "WH-A", "last_counted": "2024-01-15"})
    report = reconcile(empty(), df2)
    malformed = [r["sku"] for r in report["data_quality_issues"]["schema_mismatch"]]
    assert "SKU005" in malformed


# --- Test 12: malformed SKU preserved in reconciliation (appears as added) ---

def test_malformed_sku_appears_as_added():
    df2 = s2({"sku": "SKU005", "name": "Widget A", "quantity": 10, "location": "WH-A", "last_counted": "2024-01-15"})
    report = reconcile(empty(), df2)
    added_skus = [r["sku"] for r in report["added"]]
    assert "SKU005" in added_skus


# --- Test 13: whitespace stripped before comparison ---

def test_whitespace_stripped_before_comparison():
    df1 = s1({"sku": "SKU-001", "name": "Widget A",    "quantity": 100, "location": "WH-A", "last_counted": "2024-01-08"})
    df2 = s2({"sku": "SKU-001", "name": " Widget A ",  "quantity": 100, "location": "WH-A", "last_counted": "2024-01-15"})
    report = reconcile(df1, df2)
    assert len(report["unchanged"]) == 1
    assert len(report["data_quality_issues"]["conflicting_descriptions_for_sku"]) == 0


# --- Test 14: output has required keys ---

def test_output_has_required_keys():
    report = reconcile(empty(), empty())
    assert "summary" in report
    assert "unchanged" in report
    assert "changed" in report
    assert "added" in report
    assert "removed" in report
    assert "data_quality_issues" in report


# --- Test 15: summary counts match list lengths ---

def test_summary_counts_match_lists():
    df1 = s1(
        {"sku": "SKU-001", "name": "Widget A", "quantity": 100, "location": "WH-A", "last_counted": "2024-01-08"},
        {"sku": "SKU-002", "name": "Widget B", "quantity": 50,  "location": "WH-A", "last_counted": "2024-01-08"},
    )
    df2 = s2(
        {"sku": "SKU-001", "name": "Widget A", "quantity": 90, "location": "WH-A", "last_counted": "2024-01-15"},
        {"sku": "SKU-003", "name": "Widget C", "quantity": 30, "location": "WH-B", "last_counted": "2024-01-15"},
    )
    report = reconcile(df1, df2)
    assert report["summary"]["unchanged"] == len(report["unchanged"])
    assert report["summary"]["changed"]   == len(report["changed"])
    assert report["summary"]["added"]     == len(report["added"])
    assert report["summary"]["removed"]   == len(report["removed"])
