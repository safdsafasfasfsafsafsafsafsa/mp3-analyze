# from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])

# # Members API Route
# @app.route("/")
# def members():
#     return {"members": ["Member1", "Member2", "Member3"]}

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import librosa
import numpy as np
from pydub import AudioSegment
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 파일 확장자 확인 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# wav, flac -> mp3 자동 변환 함수
def convert_to_mp3(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    if ext == 'mp3':
        return filepath  # 변환 필요 없음

    sound = AudioSegment.from_file(filepath, format=ext)
    mp3_path = filepath.rsplit('.', 1)[0] + '.mp3'
    sound.export(mp3_path, format='mp3')
    os.remove(filepath)  # 원본 제거
    return mp3_path

# 분석 함수
def analyze_audio(path):
    y, sr = librosa.load(path, sr=None)

    # BPM 추출
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Duration
    duration = librosa.get_duration(y=y, sr=sr)
    duration_str = f"{int(duration // 60)}:{int(duration % 60):02}"

    # Rhythm Density
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    rhythm_density = len(beat_times) / (duration / 60)

    # RMS Energy
    rms = librosa.feature.rms(y=y)[0]
    avg_rms = float(np.mean(rms))

    # Crest Factor
    peak = np.max(np.abs(y))
    crest_factor = float(peak / avg_rms) if avg_rms != 0 else 0

    # Mixing 성향 분류 (간단 버전)
    if crest_factor < 2.0:
        mixing_type = "매우 압축된 믹싱 (EDM, Trap 등)"
    elif crest_factor < 3.0:
        mixing_type = "적당히 압축된 믹싱 (Pop, House 등)"
    elif crest_factor < 4.0:
        mixing_type = "자연스러운 다이내믹 (Acoustic, Funk 등)"
    elif crest_factor < 6.0:
        mixing_type = "다이내믹 강조 믹싱 (Jazz, Rock 등)"
    else:
        mixing_type = "극단적 다이내믹 (클래식, 언프로세스드 등)"

    return {
        "bpm": round(float(tempo), 1),
        "duration": duration_str,
        "rhythm_density": round(rhythm_density, 2),
        "crest_factor": round(crest_factor, 2),
        "mixing_type": mixing_type
    }

# 업로드 및 분석 API
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

    # 필요시 mp3로 변환
    filepath = convert_to_mp3(filepath)

    result = analyze_audio(filepath)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)