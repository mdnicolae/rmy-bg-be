import os
import time
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
    output = remove(input, session=session)

    output_path = 'output.png'
    with open(output_path, 'wb') as o:
        o.write(output)

    return send_file(output_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
