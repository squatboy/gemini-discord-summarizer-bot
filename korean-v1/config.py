import os
from dotenv import load_dotenv
import pytz

load_dotenv()

# 환경 변수 로드
# .env 파일에서 환경 변수를 로드합니다
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TARGET_CHANNEL_ID_STR = os.getenv("TARGET_CHANNEL_ID")

# 설정된 시간대 (기본값: Asia/Seoul)
TIMEZONE_STR = "Asia/Seoul"
try:
    TIMEZONE = pytz.timezone(TIMEZONE_STR)
    print(f"설정된 시간대: {TIMEZONE}")
except pytz.UnknownTimeZoneError:
    print(f"경고: 알 수 없는 시간대 '{TIMEZONE_STR}'. UTC를 사용합니다.")
    TIMEZONE = pytz.utc


# 필수 환경 변수 확인
if not DISCORD_TOKEN:
    raise ValueError("환경 변수 'DISCORD_TOKEN'이 설정되지 않았습니다.")
if not GOOGLE_API_KEY:
    raise ValueError("환경 변수 'GOOGLE_API_KEY'가 설정되지 않았습니다.")
if not TARGET_CHANNEL_ID_STR:
    raise ValueError("환경 변수 'TARGET_CHANNEL_ID'가 설정되지 않았습니다.")

# 채널 ID를 정수로 변환
try:
    TARGET_CHANNEL_ID = int(TARGET_CHANNEL_ID_STR)
except ValueError:
    raise ValueError("환경 변수 'TARGET_CHANNEL_ID'가 유효한 정수(채널 ID)가 아닙니다.")

GEMINI_MODEL_NAME = "gemini-2.0-flash"
MESSAGE_FETCH_LIMIT = 1000  # 한 번에 가져올 최대 메시지 수
SUMMARY_PROMPT = """다음 Discord 채널 대화 내용을 한국어로 요약해 주세요. 중요한 논점, 결정 사항, 주요 활동 등을 중심으로 간결하게 정리해 주세요.

--- 대화 내용 시작 ---
{text}
--- 대화 내용 끝 ---

요약:"""
