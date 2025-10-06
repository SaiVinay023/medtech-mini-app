"""
backend/processing.py
---------------------
Image processing helpers used by `backend/app.py`.

This module intentionally keeps processing simple and deterministic so unit
tests can validate output shape and file format. It mixes OpenCV (fast array
ops) with PIL (I/O and a few filters) — note the BGR<->RGB conversions.

Functions:
- to_cv / to_pil: conversion helpers between PIL.Image and OpenCV numpy arrays
- arterial_enhance: applies CLAHE on L-channel in LAB colorspace and boosts
  contrast slightly. Tuned for demonstration of "arterial" enhancement.
- venous_smooth: light Gaussian blur to simulate venous-phase smoothing.
- pil_to_png_bytes: returns PNG bytes (used by the Flask response).

Tests: See `backend/tests/test_processing.py` which asserts returned objects are
PIL Images and that `pil_to_png_bytes` produces PNG-identified bytes (\x89PNG).
"""

from io import BytesIO
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import cv2


def to_pil(img: np.ndarray) -> Image.Image:
    """Convert an OpenCV BGR ndarray to a PIL RGB Image.

    Input shape: (H, W, 3), dtype=uint8. Handles BGR ordering used by cv2.
    """
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def to_cv(img_pil: Image.Image) -> np.ndarray:
    """Convert a PIL Image (RGB or L) to an OpenCV BGR ndarray.

    We keep 3 channels (BGR) for consistency with OpenCV color transforms.
    """
    arr = np.array(img_pil)
    if arr.ndim == 2:
        return cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def arterial_enhance(pil_img: Image.Image) -> Image.Image:
    """Apply simple arterial-like enhancement.

    Steps:
    - Convert to OpenCV BGR ndarray
    - Convert to LAB, apply CLAHE to L channel (local contrast)
    - Convert back to BGR, to PIL and slightly boost contrast via PIL
    """
    img = to_cv(pil_img)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # CLAHE parameters chosen for moderate enhancement in demo images
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    pil = to_pil(enhanced)
    enhancer = ImageEnhance.Contrast(pil)
    pil = enhancer.enhance(1.15)
    return pil


def venous_smooth(pil_img: Image.Image, sigma: float = 2.5) -> Image.Image:
    """Return a blurred version of the image to simulate venous-phase smoothing.

    The default sigma is moderate to produce a visible but not destructive blur.
    """
    return pil_img.filter(ImageFilter.GaussianBlur(radius=sigma))


def pil_to_png_bytes(pil_img: Image.Image, optimize=True) -> bytes:
    """Serialize a PIL Image to PNG bytes suitable for HTTP response.

    The tests assert the output begins with PNG magic bytes.
    """
    buf = BytesIO()
    pil_img.save(buf, format='PNG', optimize=optimize)
    return buf.getvalue()
