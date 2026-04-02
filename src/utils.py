"""
utils.py
--------
Shared utility functions used across the video analysis pipeline.

Functions
---------
moving_average        : Simple box-kernel moving average for 1D signals.
smooth_1d             : 1D Gaussian smoothing via OpenCV.
find_significant_peaks: Detect and merge locally significant gradient peaks.
"""

import numpy as np
import cv2


# ---------------------------------------------------------------------------
# Signal smoothing
# ---------------------------------------------------------------------------

def moving_average(x, w=11):
    """Apply a box-kernel moving average to a 1D array.

    Parameters
    ----------
    x : array-like
        Input signal (e.g., frame-by-frame foam height).
    w : int
        Window size in samples.

    Returns
    -------
    np.ndarray
        Smoothed signal with the same length as *x*.
        For very short signals (len < w), the original array is returned.
    """
    x = np.array(x, dtype=float)
    if len(x) < w:
        return x
    return np.convolve(x, np.ones(w) / w, mode="same")


def smooth_1d(arr, ksize=9):
    """Apply 1D Gaussian smoothing to a 1D array using OpenCV.

    The array is treated as a column vector so that OpenCV's 2D Gaussian
    kernel can be applied along the single non-trivial axis.

    Parameters
    ----------
    arr : array-like
        Input 1D array (e.g., vertical intensity profile).
    ksize : int
        Gaussian kernel size (must be a positive odd integer).

    Returns
    -------
    np.ndarray
        Smoothed 1D array of the same length as *arr*.
    """
    arr = np.asarray(arr, dtype=np.float32).reshape(-1, 1)
    smoothed = cv2.GaussianBlur(arr, (1, ksize), 0)
    return smoothed.flatten()


# ---------------------------------------------------------------------------
# Peak detection
# ---------------------------------------------------------------------------

def find_significant_peaks(signal, min_peak_value=2.0, min_distance=12):
    """Find locally significant peaks in a 1D signal.

    A candidate peak is a local maximum whose value meets or exceeds
    *min_peak_value*.  When two candidates lie within *min_distance* samples
    of each other, only the stronger one is retained.

    Parameters
    ----------
    signal : array-like
        Input 1D signal (e.g., absolute gradient of the vertical intensity
        profile, used to locate air/foam/liquid interfaces).
    min_peak_value : float
        Minimum amplitude for a local maximum to be considered a peak.
    min_distance : int
        Minimum number of samples between retained peaks.

    Returns
    -------
    list of int
        Indices of retained peaks in ascending order.
    """
    signal = np.asarray(signal)
    candidates = []

    # Identify local maxima above the amplitude threshold
    for i in range(1, len(signal) - 1):
        if signal[i] > signal[i - 1] and signal[i] >= signal[i + 1]:
            if signal[i] >= min_peak_value:
                candidates.append(i)

    if not candidates:
        return []

    # Merge peaks that are closer than min_distance, keeping the stronger one
    merged = []
    for p in candidates:
        if not merged:
            merged.append(p)
        elif p - merged[-1] < min_distance:
            if signal[p] > signal[merged[-1]]:
                merged[-1] = p
        else:
            merged.append(p)

    return merged
