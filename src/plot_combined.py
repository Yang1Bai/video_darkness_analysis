"""
plot_combined.py
----------------
Overlay foam-thickness and darkness-feature time series on a dual-axis figure.

Left axis  : Foam thickness in pixels (raw and smoothed).
Right axis : Darkness features â dark_ratio, darkness, std_gray_norm â all
             normalized to the range [0, 1].

The script reads the CSV files produced by analyze_foam.py and
analyze_darkness.py (or smooth_features.py).  Both CSVs must share a common
time axis; the foam CSV is used as the reference time vector.

Output
------
An interactive matplotlib window, or a saved figure if --output is specified.

Usage
-----
    python plot_combined.py [--foam FOAM_CSV] [--darkness DARKNESS_CSV] [options]

Examples
--------
    # Interactive plot with default file names
    python plot_combined.py

    # Use smoothed darkness features and save figure
    python plot_combined.py \\
        --foam ../results/InCl3_noZn_0302_foam.csv \\
        --darkness ../results/InCl3_noZn_0302_darkness_smooth.csv \\
        --output ../results/InCl3_noZn_0302_combined.png \\
        --title "InCl3 (no Zn) â 03/02"
"""

import argparse
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser(
        description="Combined dual-axis plot: foam thickness and darkness features.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--foam", default="foam_features.csv",
        help="Foam feature CSV produced by analyze_foam.py.",
    )
    parser.add_argument(
        "--darkness", default="darkness_features.csv",
        help="Darkness feature CSV produced by analyze_darkness.py "
             "(or darkness_features_smooth.csv from smooth_features.py).",
    )
    parser.add_argument(
        "--output", default=None,
        help="Save the figure to this path (e.g. combined_plot.png). "
             "If omitted, the figure is displayed interactively.",
    )
    parser.add_argument(
        "--dpi", type=int, default=150,
        help="Resolution of the saved figure in dots per inch.",
    )
    parser.add_argument(
        "--title", default="",
        help="Optional figure title.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    for path, label in [(args.foam, "foam"), (args.darkness, "darkness")]:
        if not os.path.isfile(path):
            print(f"ERROR: {label} CSV not found: {path}", file=sys.stderr)
            sys.exit(1)

    foam  = pd.read_csv(args.foam)
    video = pd.read_csv(args.darkness)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # --- Left axis: foam thickness ---
    ax1.plot(
        foam["time_s"], foam["foam_height_px"],
        alpha=0.25, color="tab:blue",
        label="foam height (raw)",
    )
    ax1.plot(
        foam["time_s"], foam["foam_height_smooth"],
        linewidth=2, color="tab:red",
        label="foam height (smooth)",
    )
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Foam thickness (pixels)")

    # --- Right axis: darkness features ---
    ax2 = ax1.twinx()
    ax2.plot(video["time_s"], video["dark_ratio"],    color="tab:orange", label="dark_ratio")
    ax2.plot(video["time_s"], video["darkness"],      color="tab:green",  label="darkness")
    ax2.plot(video["time_s"], video["std_gray_norm"], color="tab:purple", label="std_gray_norm")
    ax2.set_ylabel("Video feature value (normalized)")

    # Merge legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    if args.title:
        plt.title(args.title)

    plt.tight_layout()

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        plt.savefig(args.output, dpi=args.dpi)
        print(f"Figure saved to: {args.output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
"""
plot_combined.py
----------------
Overlay foam-thickness and darkness-feature time series on a dual-axis figure.

Left axis  : Foam thickness in pixels (raw and smoothed).
Right axis : Darkness features â dark_ratio, darkness, std_gray_norm â all
             normalized to the range [0, 1].

The script reads the CSV files produced by analyze_foam.py and
analyze_darkness.py (or smooth_features.py).  Both CSVs must share a common
time axis; the foam CSV is used as the reference time vector.

Output
------
An interactive matplotlib window, or a saved figure if --output is specified.

Usage
-----
    python plot_combined.py [--foam FOAM_CSV] [--darkness DARKNESS_CSV] [options]

Examples
--------
    # Interactive plot with default file names
    python plot_combined.py

    # Use smoothed darkness features and save figure
    python plot_combined.py \\
        --foam ../results/InCl3_noZn_0302_foam.csv \\
        --darkness ../results/InCl3_noZn_0302_darkness_smooth.csv \\
        --output ../results/InCl3_noZn_0302_combined.png \\
        --title "InCl3 (no Zn) â 03/02"
"""

import argparse
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser(
        description="Combined dual-axis plot: foam thickness and darkness features.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--foam", default="foam_features.csv",
        help="Foam feature CSV produced by analyze_foam.py.",
    )
    parser.add_argument(
        "--darkness", default="darkness_features.csv",
        help="Darkness feature CSV produced by analyze_darkness.py "
             "(or darkness_features_smooth.csv from smooth_features.py).",
    )
    parser.add_argument(
        "--output", default=None,
        help="Save the figure to this path (e.g. combined_plot.png). "
             "If omitted, the figure is displayed interactively.",
    )
    parser.add_argument(
        "--dpi", type=int, default=150,
        help="Resolution of the saved figure in dots per inch.",
    )
    parser.add_argument(
        "--title", default="",
        help="Optional figure title.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    for path, label in [(args.foam, "foam"), (args.darkness, "darkness")]:
        if not os.path.isfile(path):
            print(f"ERROR: {label} CSV not found: {path}", file=sys.stderr)
            sys.exit(1)

    foam  = pd.read_csv(args.foam)
    video = pd.read_csv(args.darkness)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # --- Left axis: foam thickness ---
    ax1.plot(
        foam["time_s"], foam["foam_height_px"],
        alpha=0.25, color="tab:blue",
        label="foam height (raw)",
    )
    ax1.plot(
        foam["time_s"], foam["foam_height_smooth"],
        linewidth=2, color="tab:red",
        label="foam height (smooth)",
    )
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Foam thickness (pixels)")

    # --- Right axis: darkness features ---
    ax2 = ax1.twinx()
    ax2.plot(video["time_s"], video["dark_ratio"],    color="tab:orange", label="dark_ratio")
    ax2.plot(video["time_s"], video["darkness"],      color="tab:green",  label="darkness")
    ax2.plot(video["time_s"], video["std_gray_norm"], color="tab:purple", label="std_gray_norm")
    ax2.set_ylabel("Video feature value (normalized)")

    # Merge legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    if args.title:
        plt.title(args.title)

    plt.tight_layout()

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        plt.savefig(args.output, dpi=args.dpi)
        print(f"Figure saved to: {args.output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
