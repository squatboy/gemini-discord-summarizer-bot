import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL_NAME, SUMMARY_PROMPT

# Google AI 설정
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    print("Google AI (Gemini) 모델이 성공적으로 설정되었습니다.")
except Exception as e:
    print(f"Google AI 설정 중 오류 발생: {e}")
    # 필요시 여기서 프로그램을 종료하거나, 기본값으로 동작하도록 처리
    model = None  # 모델 사용 불가 상태 표시


async def get_summary_from_gemini(text_to_summarize: str) -> str | None:
    """주어진 텍스트를 Gemini 모델을 이용해 요약합니다."""
    if not model:
        print("오류: Gemini 모델이 초기화되지 않았습니다.")
        return None
    if not text_to_summarize:
        print("정보: 요약할 텍스트 내용이 없습니다.")
        return None

    prompt = SUMMARY_PROMPT.format(text=text_to_summarize)

    try:
        print(f"Gemini API 호출: {len(text_to_summarize)}자 요약 요청 중...")
        response = await model.generate_content_async(prompt)
        print("Gemini API 응답 받음.")
        return response.text
    except Exception as e:
        print(f"Gemini API 호출 중 오류 발생: {e}")
        return None  # 오류 발생 시 None 반환
