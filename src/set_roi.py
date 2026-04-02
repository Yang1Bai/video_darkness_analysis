"""
set_roi.py
----------
Overlay a rectangular region-of-interest (ROI) on a reference frame and save
the annotated image.

Use this script after check_video.py to visually confirm that the ROI
coordinates are correctly placed on the reaction vessel before running the
analysis scripts.  The ROI is drawn as a red rectangle on the reference frame.

Output
------
An annotated JPEG image with the ROI overlaid (default: roi_check.jpg).

Usage
-----
    python set_roi.py --image IMAGE_PATH --roi X Y W H [--output OUTPUT_PATH]

Arguments
---------
--image  : Path to the reference frame (e.g., first_frame.jpg from check_video.py).
--roi    : Four integers defining the ROI: x y width height
           (x, y) is the top-left corner in pixels; width and height are in pixels.
--output : Path for the annotated output image (default: roi_check.jpg).

Examples
--------
    # Verify darkness ROI
    python set_roi.py --image first_frame.jpg --roi 800 775 100 70

    # Verify foam strip ROI and save to a custom path
    python set_roi.py --image first_frame.jpg --roi 825 350 125 350 --output foam_roi_check.jpg
"""

import argparse
import os
import sys

import cv2


def parse_args():
    parser = argparse.ArgumentParser(
        description="Overlay and verify a rectangular ROI on a reference frame.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--image", required=True,
        help="Path to the reference frame image (JPEG or PNG).",
    )
    parser.add_argument(
        "--roi", type=int, nargs=4, required=True,
        metavar=("X", "Y", "W", "H"),
        help="ROI coordinates: x y width height (top-left corner, pixels).",
    )
    parser.add_argument(
        "--output", default="roi_check.jpg",
        help="Output path for the annotated image.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    img = cv2.imread(args.image)
    if img is None:
        print(f"ERROR: Cannot open image: {args.image}", file=sys.stderr)
        sys.exit(1)

    x, y, w, h = args.roi

    # Draw ROI as a red rectangle (BGR: 0, 0, 255), 2 px line width
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imwrite(args.output, img)
    print(f"ROI check image saved to: {os.path.abspath(args.output)}")
    print(f"ROI: x={x}, y={y}, width={w}, height={h}")


if __name__ == "__main__":
    main()
