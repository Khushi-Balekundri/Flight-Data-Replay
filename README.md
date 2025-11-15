# Flight Data Replay Engine (X-Plane Compatible)

A lightweight Python project that **loads, cleans, and replays flight data** in real time — including optional visualization and X-Plane-friendly export.

This project is designed as a capstone-style demo for roles involving **flight simulation, FDR data processing, avionics software, and real-time systems** (e.g., Airbus / X-Plane ecosystem).

---

## &#x20;Features

* Load raw CSV flight data (timestamp, lat/lon, altitude, attitude, speed)
* Clean + interpolate data into a uniform time series
* Real-time replay engine with time-accurate stepping
* Optional live visualization using `matplotlib`
* Export to X-Plane-compatible replay CSV format
* Modular structure for future expansion (UDP streaming, plugin integration)

---

## Project Structure

```
flight-data-replay/
│
├── src/
│   ├── loader.py            # data loading + cleaning
│   ├── replay.py            # core replay engine
│   ├── visualize.py         # animation + plots
│   └── export_xplane.py     # convert to sim-compatible format
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

*(demo GIF placeholder — will be added once visualization is implemented)*

---

## How It Works (Short Version)

1. Loads raw flight data into pandas
2. Normalizes timestamps and resamples to a fixed frequency
3. Interpolates attitude + position fields
4. Streams rows in real time (`time.sleep(dt)`)
5. Optional: animates the current flight state frame-by-frame

---

## &#x20;Contributions

PRs welcome! Beginner-friendly and modular.

---

## 📜 License

MIT License.
