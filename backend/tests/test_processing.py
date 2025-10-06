"""
backend/tests/test_processing.py
--------------------------------
Small unit tests that validate the processing helpers return PIL Images and
that serialization produces PNG bytes. These tests are intentionally simple
— they assert types and PNG header rather than pixel-perfect transforms so
they're robust to minor algorithmic tweaks.
"""

import pytest
from PIL import Image
import numpy as np
from processing import arterial_enhance, venous_smooth, pil_to_png_bytes


@pytest.fixture
def sample_image():
    # Synthetic 128x128 RGB image with a central colored square. Deterministic
    # input is used so tests remain fast and repeatable.
    arr = np.zeros((128, 128, 3), dtype=np.uint8)
    arr[32:96, 32:96] = [120, 130, 140]
    return Image.fromarray(arr)


def test_arterial_changes(sample_image):
    out = arterial_enhance(sample_image)
    assert isinstance(out, Image.Image)
    data = pil_to_png_bytes(out)
    # PNG files start with 89 50 4E 47
    assert data.startswith(b'\x89PNG')


def test_venous_blur(sample_image):
    out = venous_smooth(sample_image, sigma=3.0)
    assert isinstance(out, Image.Image)
    data = pil_to_png_bytes(out)
    assert data.startswith(b'\x89PNG')
