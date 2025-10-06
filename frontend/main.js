const fileInput = document.getElementById('fileInput');
const submitBtn = document.getElementById('submitBtn');
const originalImg = document.getElementById('original');
const processedImg = document.getElementById('processed');
const status = document.getElementById('status');

const BACKEND_URL = "http://localhost:7860/process"; // replace with deployed backend URL

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return;
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
      const err = await resp.json().catch(()=>({error:resp.statusText}));
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
