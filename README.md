# discord-channelmessage-summarize-bot

## Intro

This project is a Discord bot that summarizes conversation history in Discord channels using the Google Gemini model. It helps users quickly grasp the essence of long conversations, making it easier to catch up on important information or missed details. It offers both immediate summary via slash commands for specific time ranges and an automatic daily summary feature for a configured channel.

## Features

* **Conversation Summarization:** Summarizes Discord channel message content using the Google Gemini API.
* **Slash Commands:** Supports slash commands for instant summarization of messages within specific time ranges (1 hour, 6 hours, 24 hours).
* **Automatic Daily Summary:** Automatically summarizes the previous day's conversation in a designated channel at midnight in the configured timezone.
* **Long Message Splitting:** Automatically splits long summary results into multiple messages to comply with Discord's message length limits.
* **Configurable:** Easy configuration via environment variables for Discord token, Google API key, target channel ID

## 📋 Table of Contents

1.  [Project Introduction](#-project-introduction)
2.  [Features](#-features)
3.  [Getting Started](#-getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
4.  [Configuration](#-configuration)
    * [.env File Setup](#env-file-setup)
5.  [Usage](#-usage)
    * [Slash Commands](#slash-commands)
    * [Automatic Daily Summary](#automatic-daily-summary)
6.  [Dependencies](#-dependencies)
7.  [Contributing](#-contributing)
8.  [License](#-license)

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
