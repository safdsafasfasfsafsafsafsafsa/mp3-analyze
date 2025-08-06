from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import librosa
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from pydub import AudioSegment
import os

app = FastAPI()

# 허용할 origin 리스트
origins = [
    "http://localhost:3000",  # 로컬 개발용
    "https://mp3-analyze.onrender.com",  # 실제 배포 도메인 (필요하면 추가)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 또는 ["*"]로 전체 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}

def allowed_file(filename):
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
    y, sr = librosa.load(path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    duration_str = f"{minutes}:{seconds:02d}"

    beats = np.atleast_1d(beat_frames)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    if beat_times.size > 0:
        rhythm_density = len(beat_frames) / (duration / 60)
    else:
        rhythm_density = 0

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

    plt.figure(figsize=(14, 4))
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

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return {
        "bpm": round(float(tempo), 1),
        "duration": duration_str,
        "rhythm_density": round(rhythm_density, 2),
        "crest_factor": round(crest_factor, 2),
        "mixing_type": mixing_type,
        "image": image_base64
    }

@app.get('/')
async def index():
    return {"status": "running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        if not allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")
        
        print(f"[INFO] Filename: {file.filename}")
        contents = await file.read()
        print(f"[INFO] File size: {len(contents)} bytes")

        # tmp_path = f"/tmp/{file.filename}"
        # with open(tmp_path, "wb") as f:
        #     f.write(contents)
        # mp3_path = convert_to_mp3(tmp_path)
        # result = analyze_audio(mp3_path)
        # os.remove(mp3_path)
        # return result
    
        return {"filename": file.filename, "size": len(contents)}
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {"error": str(e)}