"""
smooth_features.py
------------------
Apply centered rolling-mean smoothing to the darkness feature time series
produced by analyze_darkness.py.

The following columns are smoothed and appended to the output CSV:

  darkness_smooth    : Rolling mean of *darkness*.
  dark_ratio_smooth  : Rolling mean of *dark_ratio*.
  std_gray_smooth    : Rolling mean of *std_gray_norm*.

All other columns from the input CSV are preserved unchanged.

Usage
-----
    python smooth_features.py [--input INPUT_CSV] [--window WINDOW] [--output OUTPUT_CSV] [--plot]

Examples
--------
    # Default: window = 9, reads darkness_features.csv
    python smooth_features.py

    # Larger window, custom paths
    python smooth_features.py --input ../results/InCl3_noZn_0302_darkness.csv \\
        --window 15 --output ../results/InCl3_noZn_0302_darkness_smooth.csv

    # Preview the smoothing result
    python smooth_features.py --window 9 --plot
"""

import argparse
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser(
        description="Apply rolling-mean smoothing to darkness feature time series.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input", default="darkness_features.csv",
        help="Input CSV file produced by analyze_darkness.py.",
    )
    parser.add_argument(
        "--window", type=int, default=9,
        help="Rolling mean window size (number of time points; centered).",
    )
    parser.add_argument(
        "--output", default="darkness_features_smooth.csv",
        help="Output CSV file with smoothed columns appended.",
    )
    parser.add_argument(
        "--plot", action="store_true",
        help="Show a preview plot comparing raw and smoothed darkness.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.isfile(args.input):
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    data = pd.read_csv(args.input)
    w    = args.window

    # Centered rolling mean â edges will contain NaN (pandas default)
    data["darkness_smooth"]   = data["darkness"].rolling(window=w, center=True).mean()
    data["dark_ratio_smooth"] = data["dark_ratio"].rolling(window=w, center=True).mean()
    data["std_gray_smooth"]   = data["std_gray_norm"].rolling(window=w, center=True).mean()

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    data.to_csv(args.output, index=False)
    print(f"Smoothed features saved to: {args.output}")

    if args.plot:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data["time_s"], data["darkness"],
                alpha=0.35, color="steelblue", label="darkness (raw)")
        ax.plot(data["time_s"], data["darkness_smooth"],
                linewidth=2, color="steelblue",
                label=f"darkness (rolling mean, w={w})")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Darkness")
        ax.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
