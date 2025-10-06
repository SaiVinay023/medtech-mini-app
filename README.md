# MedTech Mini — Final README

Small demo: Flask backend (image transforms) + static frontend. The project
is deployed; use the links below to view the live app, or follow the local
setup to run the backend and tests on your machine.

Live deployment
- Frontend (Vercel): https://medtech-mini-app.vercel.app/  (open this to view the UI)
- Backend (Render): https://medtech-mini-app.onrender.com  (API endpoint base)

Repository layout (quick)
- `backend/` — Flask app and image processing helpers
  - `backend/app.py` (server + endpoints)
  - `backend/processing.py` (PIL + OpenCV helpers)
  - `backend/tests/test_processing.py` (pytest)
- `frontend/` — static UI for manual testing (`index.html`, `main.js`, `styles.css`)
- `sample_images/` — example images for curl/manual tests

Prerequisites
- Python 3.11 (see `backend/runtime.txt`)
- pip able to install binary wheels (OpenCV)

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

Viewing the deployed app
- Open the Vercel frontend: https://medtech-mini-app.vercel.app/
  - The deployed frontend is configured to call the deployed backend at
    `https://medtech-mini-app.onrender.com`. If you want to run locally you
    may need to change `BACKEND_URL` in `frontend/main.js` to `http://localhost:7860/process`.

Quick curl test (against a local server)
```bash
curl -X POST -F "image=@sample_images/CTA_Slice.jpg" -F "phase=arterial" http://localhost:7860/process --output out.png

# then open out.png with an image viewer
```

Server API summary
- POST /process with multipart/form-data
  - file field: `image` (image file)
  - form field: `phase` with value `arterial` or `venous`
- Success: returns PNG bytes (Content-Type: image/png). Errors are returned as JSON with 4xx codes.

Tests & development notes
- Tests use a deterministic synthetic image (see `backend/tests/test_processing.py`) and assert type + PNG header. Avoid pixel-perfect asserts unless you update the fixtures.
- Processing functions accept/return PIL.Image for compatibility with the Flask handler; internal ops use OpenCV arrays via `to_cv` / `to_pil`.

Troubleshooting
- If `pip install` fails on `opencv-python-headless`, upgrade pip and wheel or use a platform that provides prebuilt wheels.
- If you see CORS errors on the deployed frontend, ensure the Render backend allows requests from the frontend origin (CORS is enabled in `backend/app.py` for development).

Extras
- The assignment PDF you attached is included in the repository attachments for reference.
- If you'd like, I can add a small GitHub Actions workflow to run tests on push/PR, or a tiny `dev.ps1` helper to standardize the local dev steps.

Thank you — project is complete. View the live UI: https://medtech-mini-app.vercel.app/
