import requests
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

FASTAPI_SERVER_URL = "http://docker-fastapi-host:8000/analyze"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3', 'wav', 'flac'}

@app.route('/')
def index():
    return 'Server is running.'

@app.route('/analyze', methods=['POST'])
def upload_and_analyze():
    if 'file' not in request.files:
        return jsonify({"error": "파일이 첨부되지 않았습니다."}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "지원하지 않는 파일 형식입니다."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # FastAPI 서버로 파일 전송
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f)}
        resp = requests.post(FASTAPI_SERVER_URL, files=files)

    os.remove(filepath)

    if resp.status_code != 200:
        return jsonify({"error": "분석 서버 오류", "detail": resp.text}), 500

    return jsonify(resp.json())