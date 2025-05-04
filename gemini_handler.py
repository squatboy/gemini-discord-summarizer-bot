import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL_NAME, SUMMARY_PROMPT

# Google AI Configuration
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    print("Google AI (Gemini) model configured successfully.")
except Exception as e:
    print(f"Error configuring Google AI: {e}")
    # Optionally, terminate the program or handle with a default here
    model = None  # Indicate model is not usable


async def get_summary_from_gemini(text_to_summarize: str) -> str | None:
    """Uses the Gemini model to summarize the given text."""
    if not model:
        print("Error: Gemini model is not initialized. ❌")
        return None
    if not text_to_summarize:
        print("Info: No text content to summarize. ℹ️")
        return None

    prompt = SUMMARY_PROMPT.format(text=text_to_summarize)

    try:
        print(
            f"Calling Gemini API: Requesting summary of {len(text_to_summarize)} characters..."
        )
        response = await model.generate_content_async(prompt)
        print("Received response from Gemini API.")
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None  # Return None on error
