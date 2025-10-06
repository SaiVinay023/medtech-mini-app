# MedTech Mini — Full-stack assignment
Upload a medical image and simulate arterial or venous phase (server-side).

## Run backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
python app.py
```
Then open frontend/index.html and ensure BACKEND_URL points to http://localhost:7860/process.

## Deploy
- Backend: Hugging Face Space (or Render/Fly)
- Frontend: GitHub Pages

## Test
```bash
curl -X POST -F "image=@sample_images/CTA_Slice.jpg" -F "phase=arterial" http://localhost:7860/process --output out.png
```
