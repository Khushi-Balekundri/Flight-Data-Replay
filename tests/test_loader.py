import pandas as pd
import numpy as np
from src.loader import load_csv, normalize, interpolate
from pathlib import Path
import tempfile

# === helper ===
def make_basic_csv(path):
    """Create test CSV with minimal DataFrame operations"""
    pd.DataFrame({
        "Time": [0, 1, 2],
        "Longitude": [10, 11, 12],
        "Latitude": [20, 21, 22],
        "Altitude": [100, 110, 120],
        "Roll (deg)": [0, 1, 2],
        "Pitch (deg)": [5, 6, 7],
        "Yaw (deg)": [10, 11, 12]
    }).to_csv(path, index=False)
    return path

# === tests ===
def test_load_csv_required_columns():
    with tempfile.TemporaryDirectory() as tmp:
        df = load_csv(make_basic_csv(Path(tmp) / "test.csv"))
        assert list(df.columns) == [
            "Time", "Longitude", "Latitude", "Altitude",
            "Roll (deg)", "Pitch (deg)", "Yaw (deg)"
        ], "Column mismatch"
        print("[OK] test_load_csv_required_columns")

def test_normalize():
    result = normalize(pd.DataFrame({
        "Time": ["0", "BAD", "2"],
        "Longitude": ["10", "11", "BAD"],
        "Latitude": [20, 21, 22],
        "Altitude": [100, None, 120],
        "Roll (deg)": [0, 1, 2],
        "Pitch (deg)": [5, 6, 7],
        "Yaw (deg)": [10, 11, 12]
    }))
    assert len(result) == 1 and result.iloc[0]["Time"] == 0, "Normalize failed"
    print("[OK] test_normalize")

def test_interpolate():
    out = interpolate(pd.DataFrame({
        "Time": [0.0, 1.0],
        "Longitude": [0, 10],
        "Latitude": [0, 10],
        "Altitude": [0, 100],
        "Roll (deg)": [0, 1],
        "Pitch (deg)": [0, 1],
        "Yaw (deg)": [0, 1]
    }), rate_hz=10)
    assert np.all(np.diff(out["Time"]) > 0)
    assert len(out) == 10 and np.isclose(out["Longitude"].iloc[5], 5), "Interpolate failed"
    print("[OK] test_interpolate")

# === run tests ===
if __name__ == "__main__":
    test_load_csv_required_columns()
    test_normalize()
    test_interpolate()
    print("\nAll tests passed.\n")