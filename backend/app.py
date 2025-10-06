from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from processing import arterial_enhance, venous_smooth, pil_to_png_bytes
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Allow all origins

@app.route("/")
def index():
    return jsonify({"status": "backend ok"})

@app.route("/process", methods=["POST"])
def process_image():
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
    response.headers.set('Access-Control-Allow-Origin', '*')  # ✅ explicitly add
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
