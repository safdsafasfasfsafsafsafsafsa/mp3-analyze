# docker-compute/Dockerfile

# 1. Python 이미지 베이스로 사용
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 시스템 의존성 설치 (ffmpeg 등)
RUN apt-get update && apt-get install -y ffmpeg

# 4. requirements 복사 및 설치
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. 소스 코드 복사
COPY . .

# 6. uvicorn으로 FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]