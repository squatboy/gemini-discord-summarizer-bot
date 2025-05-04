import os
from dotenv import load_dotenv
import pytz

load_dotenv()

# Load Environment Variables
# Load environment variables from the .env file
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TARGET_CHANNEL_ID_STR = os.getenv("TARGET_CHANNEL_ID")

# Configured timezone (default: Asia/Seoul)
TIMEZONE_STR = "Asia/Seoul"
try:
    TIMEZONE = pytz.timezone(TIMEZONE_STR)
    print(f"Configured timezone: {TIMEZONE}")
except pytz.UnknownTimeZoneError:
    print(f"Warning: Unknown timezone '{TIMEZONE_STR}'. Using UTC. ⚠️")
    TIMEZONE = pytz.utc


# Check for essential environment variables
if not DISCORD_TOKEN:
    raise ValueError("Environment variable 'DISCORD_TOKEN' is not set. 🚫")
if not GOOGLE_API_KEY:
    raise ValueError("Environment variable 'GOOGLE_API_KEY' is not set. 🚫")
if not TARGET_CHANNEL_ID_STR:
    raise ValueError("Environment variable 'TARGET_CHANNEL_ID' is not set. 🚫")

# Convert channel ID to integer
try:
    TARGET_CHANNEL_ID = int(TARGET_CHANNEL_ID_STR)
except ValueError:
    raise ValueError(
        "Environment variable 'TARGET_CHANNEL_ID' is not a valid integer (channel ID). 🚫"
    )

GEMINI_MODEL_NAME = "gemini-2.0-flash"
MESSAGE_FETCH_LIMIT = 1000  # Maximum number of messages to fetch at once
SUMMARY_PROMPT = """Summarize the following Discord channel conversation in Korean. Provide a concise summary focusing on important discussion points, decisions, and key activities.

--- Conversation Start ---
{text}
--- Conversation End ---

Summary:"""
