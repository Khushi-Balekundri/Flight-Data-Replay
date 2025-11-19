import pandas as pd
import numpy as np

REQ_COLS = ['Time', 'Longitude', 'Latitude', 'Altitude',
            'Roll (deg)', 'Pitch (deg)', 'Yaw (deg)']

def load_csv(path):
    """Load flight data with required columns only."""
    df = pd.read_csv(path, usecols=lambda col: col in REQ_COLS)
    
    missing = set(REQ_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    return df[REQ_COLS]


def normalize(df):
    """Convert to numeric, remove invalid data, and sort by time."""
    # Convert all columns to numeric
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # Drop invalid rows and duplicates
    return (df.dropna()
             .sort_values("Time")
             .drop_duplicates("Time")
             .reset_index(drop=True))


def interpolate(df, rate_hz=30):
    """Resample to uniform time intervals."""
    if len(df) < 2:
        raise ValueError("Need at least 2 data points to interpolate.")
    
    # Generate new time array
    start, end = df["Time"].iloc[[0, -1]]
    new_time = np.arange(start, end, 1.0 / rate_hz)
    
    # Extract arrays once
    old_time = df["Time"].values
    
    # Build result dictionary with vectorized operations
    result = {"Time": new_time}
    for col in df.columns:
        if col != "Time":
            result[col] = np.interp(new_time, old_time, df[col].values)
    
    return pd.DataFrame(result)


def preprocess_flight_data(input_path, output_path, rate_hz=30):
    """Complete preprocessing pipeline."""
    df = load_csv(input_path)
    df = normalize(df)
    df = interpolate(df, rate_hz)
    df.to_csv(output_path, index=False)
    
    print(f"✓ Processed {len(df)} data points at {rate_hz} Hz")
    print(f"✓ Saved to: {output_path}")
    
    return output_path