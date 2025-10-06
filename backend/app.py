"""
backend/app.py
----------------
Small Flask backend for the MedTech Mini app.

Key points for contributors and AI agents:
- Exposes two endpoints: GET `/` (health) and POST `/process` which expects
  multipart/form-data with fields: `image` (file) and `phase` ('arterial'|'venous').
- Returns a PNG image (Content-Type: image/png). CORS is enabled for local
  frontend development. The backend listens on port 7860 by default.
- Image processing is delegated to `backend/processing.py` (uses OpenCV + PIL).

Run (dev):
  cd backend
  python -m venv .venv && .\.venv\Scripts\activate  # Windows PowerShell
  pip install -r requirements.txt
  python app.py

Notes:
- The frontend's `frontend/main.js` points at `http://localhost:7860/process` by
  default. Update `BACKEND_URL` there if deploying elsewhere.
"""

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from processing import arterial_enhance, venous_smooth, pil_to_png_bytes
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for dev


@app.route("/")
def index():
    """Health-check endpoint used by the frontend and CI.
    Returns a small JSON payload confirming the server is running.
    """
    return jsonify({"status": "backend ok"})


@app.route("/process", methods=["POST"])
def process_image():
    """Main image processing endpoint.

    Expects multipart/form-data with:
      - file field `image`
      - form field `phase` = 'arterial' or 'venous'

    Returns: PNG bytes with Content-Type 'image/png'. Errors are returned as
    JSON with HTTP 4xx codes.
    """
    if 'image' not in request.files:
        return jsonify({"error": "image file missing"}), 400
    phase = request.form.get('phase', '').lower()
    if phase not in ('arterial', 'venous'):
        return jsonify({"error": "phase must be 'arterial' or 'venous'"}), 400

    file = request.files['image']
    try:
        pil_img = Image.open(file.stream).convert('RGB')
    except Exception as e:
        return jsonify({"error": "cannot open image", "detail": str(e)}), 400

    if phase == 'arterial':
        out = arterial_enhance(pil_img)
    else:
        out = venous_smooth(pil_img)

    png_bytes = pil_to_png_bytes(out)
    response = make_response(png_bytes)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    # Default dev port used by the project; change if port conflicts occur.
    app.run(host="0.0.0.0", port=7860)
