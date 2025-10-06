import pytest
from PIL import Image
import numpy as np
from processing import arterial_enhance, venous_smooth, pil_to_png_bytes

@pytest.fixture
def sample_image():
    arr = np.zeros((128,128,3), dtype=np.uint8)
    arr[32:96, 32:96] = [120, 130, 140]
    return Image.fromarray(arr)

def test_arterial_changes(sample_image):
    out = arterial_enhance(sample_image)
    assert isinstance(out, Image.Image)
    data = pil_to_png_bytes(out)
    assert data.startswith(b'\x89PNG')

def test_venous_blur(sample_image):
    out = venous_smooth(sample_image, sigma=3.0)
    assert isinstance(out, Image.Image)
    data = pil_to_png_bytes(out)
    assert data.startswith(b'\x89PNG')
