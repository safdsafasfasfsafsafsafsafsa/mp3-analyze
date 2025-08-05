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

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import librosa
# import numpy as np
# from pydub import AudioSegment
# from werkzeug.utils import secure_filename
# import matplotlib.pyplot as plt
# import io
# import base64
# import traceback

# app = Flask(__name__)
# # CORS(app, origins=["http://localhost:3000"])
# CORS(app)

# UPLOAD_FOLDER = './uploads'
# ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # 파일 확장자 확인 함수
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # wav, flac -> mp3 자동 변환 함수
# def convert_to_mp3(filepath):
#     ext = filepath.rsplit('.', 1)[1].lower()
#     if ext == 'mp3':
#         return filepath  # 변환 필요 없음

#     sound = AudioSegment.from_file(filepath, format=ext)
#     mp3_path = filepath.rsplit('.', 1)[0] + '.mp3'
#     sound.export(mp3_path, format='mp3')
#     os.remove(filepath)  # 원본 제거
#     return mp3_path

# # 분석 함수
# def analyze_audio(path):
#     # 오디오 로딩
#     y, sr = librosa.load(path, sr=None)
#     minutes = int(duration // 60)
#     seconds = int(duration % 60)

#     # BPM 추출
#     tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

#     # Duration
#     duration = librosa.get_duration(y=y, sr=sr)
#     duration_str = f"{minutes}:{seconds:02d}"

#     # Rhythm Density
#     _, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
#     beats = np.atleast_1d(beats)  # 배열이 아닐 경우 강제로 배열로 변환
#     beat_times = librosa.frames_to_time(beats, sr=sr)

#     if beat_times.size > 0:
#         rhythm_density = len(beat_frames) / (duration / 60)
#     else:
#         rhythm_density = 0

#     # RMS Energy & Crest Factor
#     rms = librosa.feature.rms(y=y)[0]
#     avg_rms = float(np.mean(rms))

#     peak = np.max(np.abs(y))
#     crest_factor = float(peak / avg_rms) if avg_rms != 0 else 0

#     # Mixing 성향 분류 (간단 버전)
#     if crest_factor < 2.0:
#         mixing_type = "매우 압축된 믹싱 (EDM, Trap 등)"
#     elif crest_factor < 3.0:
#         mixing_type = "적당히 압축된 믹싱 (Pop, House 등)"
#     elif crest_factor < 4.0:
#         mixing_type = "자연스러운 다이내믹 (Acoustic, Funk 등)"
#     elif crest_factor < 6.0:
#         mixing_type = "다이내믹 강조 믹싱 (Jazz, Rock 등)"
#     else:
#         mixing_type = "극단적 다이내믹 (클래식, 언프로세스드 등)"

#     # 시각화
#     plt.figure(figsize=(14, 4))
#     times = librosa.times_like(rms, sr=sr)
#     plt.plot(times, rms, label='RMS Energy')
#     plt.vlines(beat_times, 0, np.max(rms), color='r', alpha=0.5, linestyle='--', label='Beats')
#     plt.xlabel('Time (mm:ss)')
#     plt.xticks(
#         ticks=np.arange(0, duration, 15),
#         labels=[f"{int(t//60)}:{int(t%60):02d}" for t in np.arange(0, duration, 15)]
#     )
#     plt.ylabel('Energy')
#     plt.title('RMS Energy & Beat Positions')
#     plt.legend()
#     plt.tight_layout()

#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)

#     image_base64 = base64.b64encode(buf.read()).decode('utf-8')

#     plt.close()

#     return {
#         "bpm": round(float(tempo), 1),
#         "duration": duration_str,
#         "rhythm_density": round(rhythm_density, 2),
#         "crest_factor": round(crest_factor, 2),
#         "mixing_type": mixing_type,
#         'image': image_base64
#     }

# # 호출용 api: 첫 페이지는 동작 확인만
# @app.route('/')
# def index():
#     return 'Server is running.'

# # 업로드 및 분석 API
# @app.route('/analyze', methods=['POST'])
# def upload_and_analyze():
#     try:
#         if 'file' not in request.files:
#             return jsonify({"error": "파일이 첨부되지 않았습니다."}), 400

#         file = request.files['file']
#         if file.filename == '' or not allowed_file(file.filename):
#             return jsonify({"error": "지원하지 않는 파일 형식입니다."}), 400

#         filename = secure_filename(file.filename)
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(filepath)

#         # 필요시 mp3로 변환
#         filepath = convert_to_mp3(filepath)

#         result = analyze_audio(filepath)
#         return jsonify(result)
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

# 테스트용 코드
from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
import numpy as np
import os
import logging

app = Flask(__name__)
CORS(app)  # CORS 설정

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.environ["NUMBA_DISABLE_JIT"] = "1"   # jit 충돌 테스트

logging.basicConfig(format='(%(asctime)s) %(levelname)s:%(message)s',
                    datefmt ='%m/%d %I:%M:%S %p',
                    level=logging.DEBUG)
logger = logging.getLogger()

# 호출용 api: 첫 페이지는 동작 확인만
@app.route('/')
def index():
    return 'Server is running.'

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    logger.debug('fl 1')
    file = request.files["file"]
    logger.debug('fl 2')

    # 파일 저장
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    logger.debug('fl 3')    # 여기까지는 됨

    try:
        # librosa로 오디오 로딩
        logger.debug('fl 4-1')
        y, sr = librosa.load(filepath, sr=None)
        logger.debug('fl 4-2')
        duration = librosa.get_duration(y=y, sr=sr)
        logger.debug('fl 4-3')

        # 원하는 결과값만 추출 (예: 길이, 샘플링레이트)
        result = {
            "filename": file.filename,
            "sample_rate": sr,
            "length": len(y),
            "duration_sec": duration
        }

        # 파일은 나중에 삭제하거나 캐시 폴더 정리 필요
        logger.debug('fl 5')
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500