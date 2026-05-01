"""
analyze_foam.py
---------------
Quantify foam/bubble-layer thickness from a vertical strip ROI in a video
recording of a chemical reaction.

Algorithm
---------
For every frame the script:
  1. Crops a narrow vertical strip ROI from the reaction vessel.
  2. Converts the ROI to grayscale and applies a 5×5 Gaussian blur.
  3. Computes the mean vertical intensity profile (averaged across ROI width).
  4. Smooths the profile with a 1D Gaussian kernel (ksize=9).
  5. Computes the absolute gradient of the smoothed profile to locate
     brightness transitions (interfaces between optical layers).
  6. Detects significant gradient peaks using a minimum-amplitude threshold
     and a minimum-separation constraint (see utils.find_significant_peaks).
  7. Retains the two strongest peaks as the major interfaces.

Layer classification
--------------------
  2 major interfaces → 3-layer system (air / foam / liquid) → foam present
                       Foam thickness = vertical distance between the two peaks.
  1 major interface  → 2-layer system (air / liquid)         → no foam
  0 major interfaces → unclassified (transitional or uniform) → no foam

A detected foam thickness outside [5, 180] pixels is considered a false
detection and discarded.

Outputs
-------
A CSV file with columns:
  time_s             : Elapsed time in seconds.
  foam_height_px     : Raw foam thickness in pixels (0 when no foam detected).
  foam_height_smooth : Moving-average smoothed foam thickness.

Usage
-----
    python analyze_foam.py --video VIDEO --roi X Y W H [options]

Examples
--------
    # Basic run with default parameters
    python analyze_foam.py --video ../data/InCl3_noZn_0302.mp4 --roi 800 500 125 350

    # Custom peak-detection parameters and save plot
    python analyze_foam.py --video ../data/InCl3_noZn_0302.mp4 \\
        --roi 800 500 125 350 --min_peak_value 2.5 --min_peak_distance 15 \\
        --smooth_window 15 --output ../results/InCl3_noZn_0302_foam.csv --plot
"""

import argparse
import os
import sys

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import moving_average, smooth_1d, find_significant_peaks


def parse_args():
    parser = argparse.ArgumentParser(
        description="Quantify foam thickness from a vertical strip ROI in a video.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--video", required=True,
        help="Path to the input video file.",
    )
    parser.add_argument(
        "--roi", type=int, nargs=4, required=True,
        metavar=("X", "Y", "W", "H"),
        help="Vertical strip ROI coordinates: x y width height (top-left corner, pixels).",
    )
    parser.add_argument(
        "--min_peak_value", type=float, default=2.0,
        help="Minimum gradient magnitude to qualify as a layer interface peak.",
    )
    parser.add_argument(
        "--min_peak_distance", type=int, default=12,
        help="Minimum pixel separation between two distinct interface peaks.",
    )
    parser.add_argument(
        "--smooth_window", type=int, default=15,
        help="Moving-average window size (frames) for foam height smoothing.",
    )
    parser.add_argument(
        "--output", default="foam_features.csv",
        help="Output CSV file path.",
    )
    parser.add_argument(
        "--plot", action="store_true",
        help="Show diagnostic plots after analysis.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video: {args.video}", file=sys.stderr)
        sys.exit(1)

    fps         = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width       = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Video: {args.video}")
    print(f"  FPS: {fps:.2f}  |  Frames: {frame_count}  |  Size: {width}×{height}")

    x, y, w, h = args.roi
    print(f"  ROI: x={x}, y={y}, w={w}, h={h}")

    times, foam_heights, layer_counts, major_interface_counts = [], [], [], []

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        roi  = frame[y:y + h, x:x + w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Vertical mean intensity profile (averaged across ROI width)
        profile        = np.mean(gray, axis=1)
        profile_smooth = smooth_1d(profile, ksize=9)
        grad           = np.gradient(profile_smooth)
        abs_grad       = np.abs(grad)

        # Detect interface peaks; exclude pixels within 8 px of the ROI edge
        peaks = find_significant_peaks(
            abs_grad,
            min_peak_value=args.min_peak_value,
            min_distance=args.min_peak_distance,
        )
        peaks = [p for p in peaks if 8 <= p <= h - 8]

        # Keep the two strongest peaks as the major interfaces
        if len(peaks) > 0:
            peaks_by_strength = sorted(peaks, key=lambda p: abs_grad[p], reverse=True)
            major_peaks       = sorted(peaks_by_strength[:2])
        else:
            major_peaks = []

        major_interface_count = len(major_peaks)

        # --- Layer classification and foam thickness ---
        if major_interface_count == 2:
            y_top       = major_peaks[0]
            y_bottom    = major_peaks[1]
            foam_height = y_bottom - y_top

            # Sanity check: discard physically implausible foam thickness
            if foam_height < 5 or foam_height > 180:
                foam_height = 0
                layer_count = 2          # revert to 2-layer interpretation
            else:
                layer_count = 3          # 3-layer: air / foam / liquid
        elif major_interface_count == 1:
            layer_count = 2              # 2-layer: air / liquid
            foam_height = 0
        else:
            layer_count = 1              # unclassified
            foam_height = 0

        times.append(frame_idx / fps)
        foam_heights.append(foam_height)
        layer_counts.append(layer_count)
        major_interface_counts.append(major_interface_count)

        frame_idx += 1

    cap.release()

    foam_heights_smooth = moving_average(foam_heights, w=args.smooth_window)

    data = pd.DataFrame({
        "time_s":             times,
        "foam_height_px":     foam_heights,
        "foam_height_smooth": foam_heights_smooth,
    })

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    data.to_csv(args.output, index=False)
    print(f"Foam features saved to: {args.output}  ({len(data)} frames)")

    if args.plot:
        fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

        axes[0].plot(times, foam_heights,        alpha=0.3,   label="foam_height_px (raw)")
        axes[0].plot(times, foam_heights_smooth, linewidth=2, label="foam_height_px (smooth)")
        axes[0].set_ylabel("Foam thickness (px)")
        axes[0].legend()

        axes[1].plot(times, layer_counts, alpha=0.5, label="layer_count")
        axes[1].set_ylabel("Detected layers")
        axes[1].legend()

        axes[2].plot(times, major_interface_counts, label="major_interface_count")
        axes[2].set_ylabel("Major interfaces")
        axes[2].set_xlabel("Time (s)")
        axes[2].legend()

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
