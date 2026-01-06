import argparse
import pandas as pd
from pathlib import Path

from src.loader import preprocess_flight_data
from src.replay import compute_xyz
from src.visualize import plot_map, plot_trajectory, plot_attitude, animate_trajectory
from src.export_replay_fdr import write_replay_fdr

def main():
    parser = argparse.ArgumentParser(
        description="Flight Data Replay Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--input", required=True, help="Raw input CSV file")
    parser.add_argument("--clean", default="data/clean/cleaned.csv", 
                       help="Output cleaned CSV path")
    parser.add_argument("--fdr", default=None, help="Optional output .fdr file path")
    parser.add_argument("--skip-viz", action="store_true", 
                       help="Skip visualizations (faster processing)")
    parser.add_argument("--force-reprocess", action="store_true",
                       help="Force reprocessing even if clean file exists")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Flight Data Replay Pipeline")
    print("=" * 60)
    
    # Smart loading: skip preprocessing if clean file exists
    if not args.force_reprocess and Path(args.clean).exists():
        print("\n[1/4] Loading existing cleaned data...")
        df = pd.read_csv(args.clean)
        
        # Check if XYZ already computed
        if all(col in df.columns for col in ["X", "Y", "Z"]) and not df[["X","Y","Z"]].isna().all().any():

            print(" XYZ coordinates already present")
        else:
            print("[2/4] Computing ECEF coordinates...")
            df = compute_xyz(df)
            df.to_csv(args.clean, index=False)
    else:
        # Full preprocessing
        print("\n[1/4] Preprocessing flight data...")
        preprocess_flight_data(args.input, args.clean)
        
        print("[2/4] Computing ECEF coordinates...")
        df = pd.read_csv(args.clean)
        df = compute_xyz(df)
        df.to_csv(args.clean, index=False)
    
    # Visualizations
    if not args.skip_viz:
        print("[3/4] Generating visualizations...")
        plot_map(df)
        plot_attitude(df)
        plot_trajectory(df)
        animate_trajectory(df)
    else:
        print("[3/4] Skipping visualizations")
    
    # Export
    print("[4/4] Exporting files...")
    if args.fdr is None:
        default = "data/out.fdr"
        print(f"No --fdr provided — writing to {default}")
        args.fdr = default
    write_replay_fdr(df, args.fdr)
    print(f"  Generated FDR file: {args.fdr}")

    
    print(f"\n{'=' * 60}")
    print(f" Pipeline complete!")
    print(f" Cleaned data: {args.clean}")
    print(f" Total data points: {len(df):,}")
    print(f" Duration: {df['Time'].max() - df['Time'].min():.1f} seconds")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()