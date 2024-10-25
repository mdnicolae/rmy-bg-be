import os
import time
import pyheif
import io

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

    input = file.read()
    # if file is type heif or heic, convert to png
    name_lower = file.filename.lower()
    # check if file type is supported
    supported_types = ['.png', '.jpg', '.jpeg', '.heif', '.heic']
    if not any(name_lower.endswith(t) for t in supported_types):
        return "Unsupported file type"

    if name_lower.endswith('.heif') or name_lower.endswith('.heic'):
        input = convert_heif(input)

    output = remove(input, session=session)

    output_path = 'output.png'
    with open(output_path, 'wb') as o:
        o.write(output)

    return send_file(output_path, as_attachment=True)

def convert_heif(input):
    heif_file = pyheif.read_heif(io.BytesIO(input))
    image = heif_file.convert_to_pil()
    image.save('temp.png', 'PNG')
    with open('temp.png', 'rb') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
