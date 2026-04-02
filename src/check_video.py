"""
check_video.py
--------------
Inspect video metadata and export selected frames for ROI setup.

Run this script first to confirm that the video can be opened and to obtain
reference frames that are used by set_roi.py to verify ROI placement.

Outputs
-------
<output_dir>/first_frame.jpg
    The very first frame of the video.
<output_dir>/frame_<t>s.jpg
    The frame nearest to *--target_time* seconds into the video.

Usage
-----
    python check_video.py --video VIDEO_PATH [--target_time SECONDS] [--output_dir DIR]

Examples
--------
    # Inspect a video and export frames at 0 s and 9 s
    python check_video.py --video ../data/InCl3_noZn_0302.mp4

    # Export a frame at a custom time and save to a specific folder
    python check_video.py --video ../data/InCl3_noZn_0302.mp4 --target_time 15 --output_dir ../example_output
"""

import argparse
import os
import sys

import cv2


def parse_args():
    parser = argparse.ArgumentParser(
        description="Inspect video metadata and export reference frames.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--video", required=True,
        help="Path to the input video file.",
    )
    parser.add_argument(
        "--target_time", type=float, default=9.0,
        help="Time (s) of the additional reference frame to export.",
    )
    parser.add_argument(
        "--output_dir", default=".",
        help="Directory in which exported frames are saved.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Opening video: {args.video}")
    cap = cv2.VideoCapture(args.video)

    if not cap.isOpened():
        print(f"ERROR: Cannot open video: {args.video}", file=sys.stderr)
        sys.exit(1)

    fps         = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width       = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration    = frame_count / fps if fps > 0 else 0.0

    print(f"  FPS:         {fps:.2f}")
    print(f"  Frame count: {frame_count}")
    print(f"  Resolution:  {width} x {height} px")
    print(f"  Duration:    {duration:.1f} s")

    # --- Export first frame ---
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, frame = cap.read()
    if ret:
        out_path = os.path.join(args.output_dir, "first_frame.jpg")
        cv2.imwrite(out_path, frame)
        print(f"First frame saved to: {os.path.abspath(out_path)}")
    else:
        print("WARNING: Cannot read first frame.", file=sys.stderr)

    # --- Export frame at target time ---
    cap.set(cv2.CAP_PROP_POS_MSEC, args.target_time * 1000)
    ret, frame = cap.read()
    if ret:
        out_path = os.path.join(args.output_dir, f"frame_{args.target_time:.1f}s.jpg")
        cv2.imwrite(out_path, frame)
        print(f"Frame at {args.target_time} s saved to: {os.path.abspath(out_path)}")
    else:
        print(f"WARNING: Cannot read frame at {args.target_time} s.", file=sys.stderr)

    cap.release()
    print("Done.")


if __name__ == "__main__":
    main()
