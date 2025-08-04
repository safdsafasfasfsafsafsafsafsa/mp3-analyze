# 파일 업로드 (Colab 전용)
from google.colab import files
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import io

uploaded = files.upload()
for fn in uploaded.keys():
    file_path = fn

# 오디오 로딩
y, sr = librosa.load(file_path, sr=None)
duration = librosa.get_duration(y=y, sr=sr)
minutes = int(duration // 60)
seconds = int(duration % 60)
duration_str = f"{minutes}:{seconds:02d}"

# 비트 추출
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beats = np.atleast_1d(beats)  # 배열이 아닐 경우 강제로 배열로 변환
beat_times = librosa.frames_to_time(beats, sr=sr)


# 리듬 밀도 계산
if beats.size > 0:
    rhythm_density = len(beats) / (duration / 60)
else:
    rhythm_density = 0

# RMS 에너지 및 Crest Factor 계산
rms = librosa.feature.rms(y=y)[0]
rms_mean = float(np.mean(rms))
crest_factor = np.max(np.abs(y)) / (rms_mean + 1e-7)

# 믹싱 성향 판단
def classify_crest_factor(cf):
    if cf < 2.0:
        return "매우 압축된 믹싱 (EDM, Trap 등)"
    elif cf < 3.0:
        return "적당히 압축된 믹싱 (Pop, House 등)"
    elif cf < 4.0:
        return "자연스러운 다이내믹 (Acoustic, Funk 등)"
    elif cf < 6.0:
        return "다이내믹 강조 믹싱 (Jazz, Rock 등)"
    else:
        return "극단적 다이내믹 (클래식, 언프로세스드 등)"

# 출력
print(f"\n🎼 {file_path}")
print(f" - BPM: {tempo[0]:.1f}")
print(f" - Rhythm Density: {rhythm_density:.2f} (DnB / EDM / 실험적 리듬 기준)")
print(f" - Duration: {duration_str}")
print(f" - RMS 평균 에너지: {rms_mean:.4f}")
print(f" - Crest Factor: {crest_factor:.2f} ({classify_crest_factor(crest_factor)})")

# 시각화
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
plt.show()