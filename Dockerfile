# 1. 베이스 이미지 선택 (Python 3.11 슬림 버전 사용)
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 파일 복사 (먼저 requirements.txt만 복사하여 의존성 캐싱 활용)
COPY requirements.txt ./

# 4. Python 의존성 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. 나머지 프로젝트 파일 복사
COPY . .

# 6. 환경 변수 설정 
ENV DISCORD_BOT_TOKEN=""
ENV GOOGLE_API_KEY=""

# 7. 컨테이너 실행
CMD ["python", "main.py"]