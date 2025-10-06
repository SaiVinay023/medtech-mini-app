The MedTech Mini repo — concise instructions for AI coding agents
===============================================================

Keep guidance short and focused: explain the app structure, critical files,
how to run and test, and common change patterns. Avoid speculative instructions.

Architecture snapshot
- backend/: Flask app exposing GET `/` (health) and POST `/process`.
  - Key files: `backend/app.py`, `backend/processing.py`, `backend/tests/test_processing.py`.
  - `/process` expects multipart form-data: `image` (file) and `phase` ('arterial'|'venous').
  - Returns PNG bytes (Content-Type: image/png). CORS is enabled for local dev.
- frontend/: Minimal static UI used for manual testing.
  - Key files: `frontend/index.html`, `frontend/main.js`, `frontend/styles.css`.
  - `frontend/main.js` contains `BACKEND_URL` — change this when deploying.
- sample_images/: Placeholder for example images used by tests/manual curl commands.

Developer workflows (explicit commands)
- Create & activate venv (Windows PowerShell):
  cd backend
  python -m venv .venv; .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
- Run tests:
  pytest
- Run dev server (listens on 7860):
  python app.py
- Quick curl test (from repo root):
  curl -X POST -F "image=@sample_images/CTA_Slice.jpg" -F "phase=arterial" http://localhost:7860/process --output out.png

Project-specific patterns & conventions
- Image I/O and formats:
  - Processing functions accept/return PIL.Image objects. Internal fast ops use
    OpenCV arrays — see `to_cv` and `to_pil` helpers in `processing.py`.
  - When adding new transforms, keep the public function signature using PIL
    for compatibility with `app.py` and tests.
- Tests:
  - Tests are focused on deterministic behavior: they assert return types and
    that serialization yields PNG magic bytes. Avoid pixel-perfect asserts
    unless you also update the synthetic test fixture accordingly.
- Parameter choices:
  - CLAHE clipLimit and tileGridSize in `arterial_enhance` are intentionally
    modest; if you tune these, also update the unit tests or add new ones.

Integration points & external deps
- Flask backend depends on pinned packages in `backend/requirements.txt`.
- OpenCV is used (opencv-python-headless) for processing; ensure the runtime
  environment permits native wheels or use a CI image that includes them.
- For deployment:
  - `runtime.txt` declares Python 3.11. Use compatible hosting (Heroku,
    Hugging Face Spaces, Render). Ensure CORS is configured for the frontend domain.

When editing code, follow these low-risk guidelines
- Keep the public API of `backend/processing.py` (functions used by app/tests)
  stable unless updating tests. Use helper functions for conversions.
- If you change `BACKEND_URL` in `frontend/main.js`, prefer a build/env-time
  substitution during deployment; for quick patches editing the file is ok.
- Add tests for any new processing function. Use the existing `sample_image`
  fixture pattern for deterministic inputs.

Examples (explicit snippets from this repo)
- POST handler in `backend/app.py`:
  - Expects 'image' in request.files and 'phase' in form data.
  - Uses `pil_to_png_bytes` to serialize and returns Content-Type: image/png.
- CLAHE use in `backend/processing.py`:
  clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

If you need clarification
- Ask for which file to modify and whether to add tests. If a requested change
  touches image-processing math, indicate whether unit tests should assert
  properties (e.g., histogram stats) or exact output bytes.

Note: this file is derived from the repo contents (files referenced above).
If you add new processing modules or move endpoints, update this guidance.
