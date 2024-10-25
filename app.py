import os
import time
import pyheif
import io
from PIL import Image  # Import Pillow for image processing

from flask import Flask, request, send_file
from rembg import remove, new_session
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["https://unbgme.netlify.app", "https://unbg.be"])

# Create session during container startup
session = new_session(os.environ.get("SESSION_ID"))


@app.route('/api/upload', methods=['POST'])
def upload_file():
    print('Handling request at:', time.asctime())

    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    input_data = file.read()
    name_lower = file.filename.lower()

    # Check if file type is supported
    supported_types = ['.png', '.jpg', '.jpeg', '.heif', '.heic']
    if not any(name_lower.endswith(t) for t in supported_types):
        return "Unsupported file type"

    # If file is HEIC or HEIF, convert to PNG
    if name_lower.endswith(('.heif', '.heic')):
        heif_file = pyheif.read(input_data)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        # Convert to PNG and save to a bytes buffer
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)  # Move the buffer cursor to the beginning
        input_data = img_buffer.read()  # Read the PNG data into input_data

    output = remove(input_data, session=session)

    output_path = 'output.png'
    with open(output_path, 'wb') as o:
        o.write(output)

    return send_file(output_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
