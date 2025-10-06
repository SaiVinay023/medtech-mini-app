from io import BytesIO
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import cv2

def to_pil(img: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def to_cv(img_pil: Image.Image) -> np.ndarray:
    arr = np.array(img_pil)
    if arr.ndim == 2:
        return cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

def arterial_enhance(pil_img: Image.Image) -> Image.Image:
    img = to_cv(pil_img)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    merged = cv2.merge((cl,a,b))
    enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    pil = to_pil(enhanced)
    enhancer = ImageEnhance.Contrast(pil)
    pil = enhancer.enhance(1.15)
    return pil

def venous_smooth(pil_img: Image.Image, sigma: float = 2.5) -> Image.Image:
    return pil_img.filter(ImageFilter.GaussianBlur(radius=sigma))

def pil_to_png_bytes(pil_img: Image.Image, optimize=True) -> bytes:
    buf = BytesIO()
    pil_img.save(buf, format='PNG', optimize=optimize)
    return buf.getvalue()
