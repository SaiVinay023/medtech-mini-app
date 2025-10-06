# MedTech Mini — Full-stack assignment
This repository contains a minimal Flask backend that applies simple
image transforms to simulate arterial/venous phases, and a tiny static
frontend used for manual testing.

Quick developer orientation:
- Backend entry: `backend/app.py` (POST /process, returns image/png)
- Image processing: `backend/processing.py` (uses OpenCV + PIL)
- Frontend: `frontend/index.html`, `frontend/main.js` (change BACKEND_URL there)
- Tests: `backend/tests/test_processing.py` (pytest)

Run locally (Windows PowerShell):
```powershell
# MedTech Mini — Full-stack assignment

Minimal demo: a Flask backend that applies simple image transforms to
simulate arterial/venous phases and a tiny static frontend used for manual
testing.

Repository layout (quick):
- `backend/` — Flask app and image processing helpers
	- `backend/app.py` (server + endpoints)
	- `backend/processing.py` (PIL + OpenCV helpers; public functions take/return PIL.Image)
	- `backend/tests/test_processing.py` (pytest)
- `frontend/` — static UI for manual testing (`index.html`, `main.js`, `styles.css`)
- `sample_images/` — place example images for curl/manual tests

Prerequisites
- Python 3.11 (project `runtime.txt` declares 3.11)
- A modern pip that can install binary wheels (OpenCV native wheels are used)

Run locally (Windows PowerShell)
```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# run tests
pytest -q

# start dev server (listens on 7860)
python app.py
```

Run locally (macOS / Linux / WSL)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python app.py
```

How to use the frontend
- Open `frontend/index.html` in your browser for a quick manual UI.
- By default `frontend/main.js` points to the local backend:
	```js
	const BACKEND_URL = "http://localhost:7860/process"
	```
	Update that string when the backend is deployed.

Quick curl test (from repo root)
```bash
curl -X POST -F "image=@sample_images/CTA_Slice.jpg" -F "phase=arterial" http://localhost:7860/process --output out.png

# then open out.png with an image viewer
```

What the server expects
- POST /process with multipart/form-data
	- file field: `image` (image file)
	- form field: `phase` with value `arterial` or `venous`

What the server returns
- On success: raw PNG bytes with `Content-Type: image/png`.
- On error: JSON payload and HTTP 4xx status (e.g. missing file or invalid phase).

Tests and patterns
- Tests use a deterministic synthetic image fixture and assert that helpers
	return `PIL.Image` and that serialization begins with PNG magic bytes
	(tests avoid pixel-perfect asserts to remain robust to small algorithmic changes).
- Processing functions in `backend/processing.py` accept and return PIL Images.
	Internal operations use NumPy/OpenCV arrays; use `to_cv` / `to_pil` helpers.

Troubleshooting
- If `pip install` fails on `opencv-python-headless`, ensure your pip/newest
	wheel support is up to date and you have a compatible platform wheel.
- If the frontend shows CORS errors after deployment, make sure the backend
	allows requests from your frontend origin (see `flask_cors` usage in `app.py`).

Deployment notes
- `runtime.txt` declares Python 3.11 — pick a host that supports this runtime.
- Backend can be deployed to simple PaaS providers (Heroku, Render, Hugging
	Face Spaces). When deploying, set the production backend URL in
	`frontend/main.js` (or inject at build time) and configure CORS accordingly.

If you want, I can:
- Add a GitHub Actions workflow to run tests on push/PR.
- Add a tiny Makefile or PowerShell script to standardize dev commands.
