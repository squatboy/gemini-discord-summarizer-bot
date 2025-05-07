🇰🇷 README [한국어](#한국어)

<br>

# `discord-channelmessage-summarize-bot`

## Intro

a Discord bot that summarizes conversation history in Discord channels using the Google Gemini model. It helps users quickly grasp the essence of long conversations, making it easier to catch up on important information or missed details. It offers both immediate summary via slash commands for specific time ranges and an automatic daily summary feature for a configured channel.

## Deploy
<img width="1033" alt="discord-bot-arch" src="https://github.com/user-attachments/assets/21e1aa39-2503-40b9-a490-f2169c1f6003" />
Can be deployed in a cloud environment like above diagram. For 24/7 hosting & smaller-scale deployments, it can be easily configured with free tiers or serverless services, similar to my own setup.

```Use it as a reference only. Design an architecture that best suits your service's scale.```

## Features

* **`Conversation Summarization`:** Summarizes Discord channel message content using the Google Gemini API.
* **`Slash Commands`:** Supports slash commands for instant summarization of messages within specific time ranges (1 hour, 6 hours, 24 hours).
* **`Automatic Daily Summary`:** Automatically summarizes the previous day's conversation in a designated channel at midnight in the configured timezone.
* **`Long Message Splitting`:** Automatically splits long summary results into multiple messages to comply with Discord's message length limits.
* **`Configurable`:** Easy configuration via environment variables for Discord token, Google API key, target channel ID

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.8 or higher installed 🐍
* A Discord Bot Application created and the Bot Token 🔑
* Gemini API Key 🔑
> Enable the **Message Content Intent** for your bot in the Discord Developer Portal (under Bot settings) ✅

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/squatboy/gemini-discord-summary-bot.git
    cd gemini-discord-summary-bot
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    Install the required libraries. You will need a `requirements.txt` file containing the following:
    ```txt
    discord.py
    google-generativeai
    python-dotenv
    pytz
    ```
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

You need to create a `.env` file in the project's root directory and set the following environment variables.

### `.env` File Setup

```dotenv
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
GOOGLE_API_KEY=YOUR_GOOGLE_GEMINI_API_KEY
TARGET_CHANNEL_ID=YOUR_TARGET_CHANNEL_ID_FOR_DAILY_SUMMARY
```

## Commands
<img width="469" alt="screenshot" src="https://github.com/user-attachments/assets/33998476-c1e4-4190-aab3-4e4ffb7e0194" />



<br>

---

<br>
<br>
<br>

## 한국어

## 소개

Discord 채널의 대화 내용을 Google Gemini 모델을 활용하여 요약해 주는 Discord 봇입니다. 긴 대화 내용을 빠르게 파악하여 중요한 정보나 놓친 내용을 쉽게 확인하는 데 도움을 줍니다. 특정 시간 범위의 메시지를 즉시 요약하거나, 설정된 채널에서 매일 자동으로 전날의 대화 내용을 요약하는 기능을 제공합니다.

## 배포
<img width="1033" alt="discord-bot-arch" src="https://github.com/user-attachments/assets/c54f588a-c038-4f72-9cd8-77ee81a8ed09" />
위 다이어그램과 같이 클라우드 환경에서 배포할 수 있으며, 24/7 호스팅 & 소규모의 경우 저랑 비슷하게 free tier들로 구성하거나 serverless 서비스들로 간단하게 구성이 가능합니다


## 주요 기능

* **대화 요약:** Google Gemini API를 사용하여 Discord 채널의 메시지 내용을 요약합니다.
* **슬래시 커맨드:** 특정 시간(1시간, 6시간, 24시간) 동안의 메시지를 즉시 요약하는 슬래시 커맨드를 지원합니다.
* **자동 일일 요약:** 설정된 시간대의 자정에 특정 채널의 전날 대화 내용을 자동으로 요약하여 전송합니다.
* **긴 메시지 분할:** 요약 결과가 Discord 메시지 길이 제한을 초과할 경우 자동으로 분할하여 전송합니다.

## 시작하기

프로젝트를 로컬 환경에서 실행하기 위한 설정 방법입니다.
코드 내부 로직에 대한 설명 및 메세지 요약 언어를 한국어로 원하시면
프로젝트 내부 디렉토리 `korean-v1` 를 사용하시면 됩니다.

### 필수 조건

* Python 3.8 이상 버전 설치 🐍
* Discord 봇 애플리케이션 생성 및 봇 토큰 확보 🔑
* Gemini API 키 🔑
* Discord 봇의 메시지 내용 인텐트(Message Content Intent) 활성화 (Discord 개발자 포털에서 봇 설정에서 활성화) ✅

### 설치

1.  **저장소 클론:**
    ```bash
    git clone [프로젝트 저장소 URL]
    cd [프로젝트 폴더]
    ```

2.  **가상 환경 설정 (권장):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **종속성 설치:**
    프로젝트에 필요한 라이브러리를 설치합니다. 아래 내용을 포함하는 `requirements.txt` 파일이 필요합니다.
    ```txt
    discord.py
    google-generativeai
    python-dotenv
    pytz
    ```
    ```bash
    pip install -r requirements.txt
    ```

## 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 환경 변수를 설정해야 합니다.

### `.env` 파일 설정

```dotenv
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
GOOGLE_API_KEY=YOUR_GOOGLE_GEMINI_API_KEY
TARGET_CHANNEL_ID=YOUR_TARGET_CHANNEL_ID_FOR_DAILY_SUMMARY
