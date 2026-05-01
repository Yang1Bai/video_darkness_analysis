"""
analyze_darkness.py
-------------------
Extract darkness-related optical features from a fixed rectangular ROI in a
video recording of a chemical reaction.

For each sampled frame the script crops the ROI, converts it to grayscale,
applies a 5×5 Gaussian blur, and computes the following metrics:

  mean_gray     : Mean pixel intensity in the ROI (range 0–255).
  dark_ratio    : Fraction of pixels whose intensity falls below *--threshold*.
  darkness      : Normalized darkness index, defined as  1 − mean_gray / 255.
                  Equals 0 for a fully bright ROI and 1 for a completely dark one.
  std_gray      : Standard deviation of pixel intensities in the ROI.
  std_gray_norm : Normalized std, defined as  std_gray / 255.

Frames are sampled at a fixed time interval (*--step_time*) rather than every
frame to reduce redundancy and computation time.

Output
------
A CSV file with columns: time_s, mean_gray, dark_ratio, darkness,
std_gray, std_gray_norm.

Usage
-----
    python analyze_darkness.py --video VIDEO --roi X Y W H [options]

Examples
--------
    # Basic run with default parameters
    python analyze_darkness.py --video ../data/InCl3_noZn_0302.mp4 --roi 800 775 100 70

    # Custom threshold and sampling interval
    python analyze_darkness.py --video ../data/InCl3_noZn_0302.mp4 \\
        --roi 800 775 100 70 --threshold 65 --step_time 0.3 \\
        --output ../results/InCl3_noZn_0302_darkness.csv
"""

import argparse
import os
import sys

import cv2
import numpy as np
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract darkness features from a fixed ROI in a video.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--video", required=True,
        help="Path to the input video file.",
    )
    parser.add_argument(
        "--roi", type=int, nargs=4, required=True,
        metavar=("X", "Y", "W", "H"),
        help="ROI coordinates: x y width height (top-left corner, pixels).",
    )
    parser.add_argument(
        "--threshold", type=int, default=65,
        help="Grayscale intensity threshold for dark-pixel classification (0–255).",
    )
    parser.add_argument(
        "--step_time", type=float, default=0.3,
        help="Time interval between consecutively analyzed frames (seconds).",
    )
    parser.add_argument(
        "--output", default="darkness_features.csv",
        help="Output CSV file path.",
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

    x, y, w, h   = args.roi
    threshold     = args.threshold
    # Convert sampling interval from seconds to frames
    step_frames   = max(1, int(round(fps * args.step_time)))

    print(f"  ROI: x={x}, y={y}, w={w}, h={h}")
    print(f"  Darkness threshold: {threshold}  |  Sampling every {step_frames} frame(s)")

    times, dark_ratios, mean_grays, std_grays = [], [], [], []

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % step_frames == 0:
            # Crop ROI and convert to grayscale
            roi  = frame[y:y + h, x:x + w]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # Gaussian blur to suppress high-frequency noise before metric computation
            gray = cv2.GaussianBlur(gray, (5, 5), 0)

            # --- Feature extraction ---
            dark_ratio = np.sum(gray < threshold) / gray.size
            mean_gray  = float(np.mean(gray))
            std_gray   = float(np.std(gray))

            times.append(frame_idx / fps)
            dark_ratios.append(dark_ratio)
            mean_grays.append(mean_gray)
            std_grays.append(std_gray)

        frame_idx += 1

    cap.release()

    mean_grays_arr = np.array(mean_grays)
    std_grays_arr  = np.array(std_grays)

    data = pd.DataFrame({
        "time_s":        times,
        "mean_gray":     mean_grays_arr,
        "dark_ratio":    dark_ratios,
        # Normalized darkness index: 0 = fully bright, 1 = fully dark
        "darkness":      1.0 - mean_grays_arr / 255.0,
        "std_gray":      std_grays_arr,
        "std_gray_norm": std_grays_arr / 255.0,
    })

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    data.to_csv(args.output, index=False)
    print(f"Features saved to: {args.output}  ({len(data)} time points)")


if __name__ == "__main__":
    main()
