# Flight Data Replay Engine (Telemetry Replay System)

A telemetry replay and analysis system for processing time-sequenced flight data and simulating system behavior in a controlled environment.

Designed to emulate real-world telemetry pipelines, enabling monitoring, validation, and analysis of aircraft state over time.

This project is designed as a demo for roles involving telemetry systems, mission operations, simulation pipelines, and real-time data processing.

---

## Why this project matters

* Simulates how real-world telemetry systems ingest and process time-series data
* Enables analysis of system behavior and state transitions over time
* Demonstrates concepts relevant to mission operations, monitoring, and anomaly detection

---

## Features

* Load raw CSV flight data (timestamp, lat/lon, altitude, attitude, speed)
* Clean + interpolate data into a uniform time series
* Real-time replay engine with time-accurate stepping
* Optional live visualization using `matplotlib`
* Export to X-Plane-compatible replay CSV format
* Modular structure for future expansion (UDP streaming, plugin integration)
* Handles multi-parameter telemetry data (position, attitude)

---

## Project Structure

```
flight-data-replay/
│
├── src/
│   ├── loader.py            # data loading + cleaning
│   ├── replay.py            # core replay engine
│   ├── visualize.py         # animation + plots
│   └── export_replay_fdr.py     # convert to sim-compatible format
│
├── data/
│   ├── raw/                 # raw input files
│   └── clean/               # cleaned, interpolated output
│
├── docs/
│   └── demo.gif             # sample visualization
│
├── notebooks/
│   └── exploration.ipynb    # optional experiments
│
├── README.md                # this file
└── requirements.txt         # dependencies
```

---

## Installation

```bash
pip install -r requirements.txt
```

Dependencies include:

* pandas
* numpy
* matplotlib
* python-dateutil

---

## Usage

### **1. Run the replay engine**

```bash
python src/replay.py --input data/clean/example.csv
```

### **2. Run with visualization**

```bash
python src/replay.py --input data/clean/example.csv --visualize
```

### **3. Convert to X-Plane compatible CSV**

```bash
python src/export_xplane.py --input data/clean/example.csv --output xplane_replay.csv
```

---

## Sample Output

*(demo GIF placeholder — it will be added once visualization is implemented)*

---

## How It Works (Short Version) 

1. Loads raw flight data into pandas
2. Normalizes timestamps and resamples to a fixed frequency
3. Interpolates attitude + position fields
4. Streams time-sequenced telemetry data to emulate real-time system behavior
5. Optional: animates the current flight state frame-by-frame

---

## Contributions 

PRs welcome! Beginner-friendly and modular.

---

## License

MIT License.
