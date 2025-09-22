from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import librosa
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import io
import base64
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://bo-10000.tistory.com/entry/Librosa-musicaudio-processing-library-Librosa-%EC%82%AC%EC%9A%A9%EB%B2%95-Tutorial-3-Audio-feature-extraction

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(format='(%(asctime)s) %(levelname)s:%(message)s',
                    datefmt ='%m/%d %I:%M:%S %p',
                    level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_mp3(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    if ext == 'mp3':
        return filepath
    sound = AudioSegment.from_file(filepath, format=ext)
    mp3_path = filepath.rsplit('.', 1)[0] + '.mp3'
    sound.export(mp3_path, format='mp3')
    os.remove(filepath)
    return mp3_path

def analyze_audio(path):
    # 모듈 호출
    y, sr = librosa.load(path, sr=None)
    hop_length = 512  # 일정하게 유지

    # 곡 길이
    duration = librosa.get_duration(y=y, sr=sr)
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    duration_str = f"{minutes}:{seconds:02d}"

    # 1. bpm & 리듬 밀도
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    if beat_times.size > 0:
        rhythm_density = len(beat_frames) / (duration / 60)
    else:
        rhythm_density = 0

    # 2. 크레스트 팩터 & 믹싱 강도
    rms = librosa.feature.rms(y=y)[0]
    avg_rms = float(np.mean(rms))
    peak = np.max(np.abs(y))
    crest_factor = float(peak / avg_rms) if avg_rms != 0 else 0

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

    # 3. pitch, octave 이미지
    plt.figure(figsize=(18, 6))
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', sr=sr, hop_length=hop_length)
    plt.colorbar(format='%+2.0f dB')
    plt.title("Chromagram")
    plt.tight_layout()

    buf_pitch = io.BytesIO()
    plt.savefig(buf_pitch, format='png')
    buf_pitch.seek(0)
    pitch_image_base64 = base64.b64encode(buf_pitch.read()).decode('utf-8')
    plt.close()
    buf_pitch.close()

    # 4. RMS & 비트 이미지 생성, base64 변환
    plt.figure(figsize=(14, 6))
    times = librosa.times_like(rms, sr=sr)
    plt.plot(times, rms, label='RMS Energy')
    plt.vlines(beat_times, 0, np.max(rms), color='r', alpha=0.5, linestyle='--', label='Beats')
    plt.xlabel('Time (mm:ss)')
    plt.xticks(
        ticks=np.arange(0, duration, 15),
        labels=[f"{int(t//60)}:{int(t%60):02d}" for t in np.arange(0, duration, 15)]
    )
    plt.ylabel('Energy')
    plt.title('RMS Energy & Beat Positions')
    plt.legend()
    plt.tight_layout()

    buf_beat = io.BytesIO()
    plt.savefig(buf_beat, format='png')
    buf_beat.seek(0)
    beat_image_base64 = base64.b64encode(buf_beat.read()).decode('utf-8')
    plt.close()
    buf_beat.close()

    # 5. MFCCs 추출
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # MFCC 통계 (예: 평균)
    avg_mfccs = np.mean(mfccs, axis=1)

    # MFCCs 시각화
    plt.figure(figsize=(14, 6))
    librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()

    buf_mfcc = io.BytesIO()
    plt.savefig(buf_mfcc, format='png')
    buf_mfcc.seek(0)
    mfcc_image_base64 = base64.b64encode(buf_mfcc.read()).decode('utf-8')
    plt.close()
    buf_mfcc.close()

    return {
        "bpm": round(float(tempo), 1),
        "duration": duration_str,
        "rhythm_density": round(rhythm_density, 2),
        "crest_factor": round(crest_factor, 2),
        "mixing_type": mixing_type,
        "pitch_image": pitch_image_base64,
        "beat_image": beat_image_base64,
        "mfcc_image": mfcc_image_base64,
        "mfcc_mean": avg_mfccs.tolist()  # numpy array를 list로 변환
    }

@app.get("/")
async def index():
    return {"message": "Server is running."}

@app.post("/analyze")
async def upload_and_analyze(file: UploadFile = File(...)):
    try:
        filename = file.filename
        logger.info(f"파일 수신: {filename}")
        if not filename or not allowed_file(filename):
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            contents = await file.read()
            # logger.info(f"파일 크기: {len(contents)} bytes")
            f.write(contents)

        # 필요 시 mp3 변환
        file_path = convert_to_mp3(file_path)

        # 취합하고 json 묶어서 전달
        result = analyze_audio(file_path)

        logger.info(f"결과 전달: {result}")
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)