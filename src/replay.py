import numpy as np
from dataclasses import dataclass
from typing import Iterator
import pandas as pd

R_EARTH = 6371000  # Earth radius in meters, ECEF

def latlon_to_xyz(lat, lon, alt_m):
    """Convert lat/lon/alt to ECEF XYZ coordinates."""
    lat = np.radians(lat)
    lon = np.radians(lon)
    r = R_EARTH + alt_m
    
    x = r * np.cos(lat) * np.cos(lon)
    y = r * np.cos(lat) * np.sin(lon)
    z = r * np.sin(lat)
    
    return x, y, z


def compute_xyz(df, alt_unit="m"):
    """Add X, Y, Z coordinates to dataframe (returns new dataframe)."""
    alt = df["Altitude"].values
    if alt_unit == "ft":
        alt = alt * 0.3048
    
    x, y, z = latlon_to_xyz(
        df["Latitude"].values,
        df["Longitude"].values,
        alt
    )
    
    return df.assign(X=x, Y=y, Z=z)  


def generate_replay_frames(df):
    """Convert flight data into FDRFrame objects (required by tests)."""
    if df is None or df.empty:
        return []

    frames = []
    for r in df[[
        "Time", "Latitude", "Longitude", "Altitude",
        "Roll (deg)", "Pitch (deg)", "Yaw (deg)"
    ]].itertuples(index=False):

        frames.append(FDRFrame(
            time=float(r[0]),
            lat=float(r[1]),
            lon=float(r[2]),
            alt=float(r[3]),
            roll=float(r[4]),
            pitch=float(r[5]),
            yaw=float(r[6])
        ))

    return frames


@dataclass
class FDRFrame:
    time: float
    lat: float
    lon: float
    alt: float
    roll: float
    pitch: float
    yaw: float

def generate_fdr_frames(df: pd.DataFrame) -> Iterator[FDRFrame]:
    if df is None or df.empty:
        return iter(())
    for r in df.itertuples(index=False):
        yield FDRFrame(
            time=float(r[0]), lat=float(r[2]), lon=float(r[1]),
            alt=float(r[3]), roll=float(r[4]), pitch=float(r[5]),
            yaw=float(r[6])
        )