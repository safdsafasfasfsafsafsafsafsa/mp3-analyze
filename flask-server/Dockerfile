FROM node:18-alpine

# 작업 디렉토리 설정
WORKDIR /app

# package.json 복사 후 의존성 설치
COPY package*.json ./
RUN npm install

# 전체 코드 복사
COPY . .

# 서버 실행
CMD ["node", "server.js"]

# Render는 내부적으로 이 포트를 사용
EXPOSE 10000