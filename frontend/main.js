/*
  frontend/main.js
  ----------------
  Lightweight glue between the static UI and the Flask backend. Key notes:
  - `BACKEND_URL` points to the POST /process endpoint and is set to the
    local dev server by default: http://localhost:7860/process
  - The UI uses FormData to send a file + a `phase` field. The backend returns
    raw PNG bytes which are rendered as an object URL in the processed <img>.

  For deployment, update BACKEND_URL to the production backend URL, and
  ensure CORS is configured on the server side.
*/

const fileInput = document.getElementById('fileInput');
const submitBtn = document.getElementById('submitBtn');
const originalImg = document.getElementById('original');
const processedImg = document.getElementById('processed');
const status = document.getElementById('status');

// Default local dev backend. Change this for deployed environments.
const BACKEND_URL = "http://localhost:7860/process";

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return;
  // Show the selected image on the left pane without uploading
  originalImg.src = URL.createObjectURL(file);
});

submitBtn.addEventListener('click', async () => {
  const file = fileInput.files[0];
  if (!file) {
    status.textContent = "Please choose an image first.";
    return;
  }
  const phase = document.querySelector('input[name="phase"]:checked').value;
  status.textContent = "Uploading and processing...";

  const form = new FormData();
  form.append('image', file);
  form.append('phase', phase);

  try {
    const resp = await fetch(BACKEND_URL, { method: 'POST', body: form });
    if (!resp.ok) {
      // Backend returns JSON errors on 4xx; attempt to parse
      const err = await resp.json().catch(() => ({ error: resp.statusText }));
      status.textContent = "Server error: " + (err.error || resp.statusText);
      return;
    }
    const blob = await resp.blob();
    processedImg.src = URL.createObjectURL(blob);
    status.textContent = "Done.";
  } catch (e) {
    status.textContent = "Network error: " + e.message;
  }
});
