from src.export_replay_fdr import write_replay_fdr
import pandas as pd

HEADER = [
    "A",
    "1000 Version",
    "FDR Created by Flight Data Replay Project",
    "I",
    "Time,Longitude,Latitude,Altitude,Roll,Pitch,Yaw",
    "DATA"
]

TEST_DF_SIMPLE = pd.DataFrame(
    [[0, 1, 2, 3, 4, 5, 6]],
    columns=["Time", "Longitude", "Latitude", "Altitude", "Roll (deg)", "Pitch (deg)", "Yaw (deg)"]
)

TEST_DF_PRECISION = pd.DataFrame(
    [[1.23456, 12.345678, 98.765432, 123.456, 1.11, 2.22, 3.33]],
    columns=["Time", "Longitude", "Latitude", "Altitude", "Roll (deg)", "Pitch (deg)", "Yaw (deg)"]
)

def test_fdr_header(tmp_path):
    fdr_path = tmp_path / "out.fdr"
    write_replay_fdr(TEST_DF_SIMPLE, fdr_path)
    
    lines = [l.strip() for l in fdr_path.read_text().splitlines()]
    assert lines[:6] == HEADER

def test_fdr_data_format(tmp_path):
    fdr_path = tmp_path / "out.fdr"
    write_replay_fdr(TEST_DF_PRECISION, fdr_path)
    
    data = fdr_path.read_text().splitlines()[-1].strip()
    parts = data.split(",")
    
    expected = ["1.235", "12.345678", "98.765432", "123.46", "1.11", "2.22", "3.33"]
    assert parts == expected, f"Expected {expected}, got {parts}"