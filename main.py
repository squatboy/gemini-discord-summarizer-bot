import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
from config import DISCORD_TOKEN

# Discord Bot Configuration
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True


class SummaryBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced successfully!")


bot = SummaryBot()


@bot.event
async def on_ready():
    """Event triggered when the bot is ready"""
    print(f"Logged in as: {bot.user.name} (ID: {bot.user.id})")
    print(f"discord.py version: {discord.__version__}")
    print("------")
    await bot.change_presence(
        activity=discord.Game(name="/summarize | Summarize Conversations")
    )


async def load_extensions():
    """Loads all Cogs within the cogs folder."""
    cogs_path = "cogs"
    for filename in os.listdir(cogs_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            try:
                # Convert file path to module path format (e.g., cogs/summary.py -> cogs.summary)
                await bot.load_extension(f"{cogs_path}.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load {filename[:-3]} Cog. ❌")
                print(f"[Error] {e}")


async def main():
    """Starts the bot and loads Cogs."""
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down bot...")
    except ValueError as e:  # Handle error raised in config.py
        print(f"Configuration error: {e}")
    except discord.LoginFailure:
        print("Discord login failed: Invalid token or network issue. 🔑")
    except Exception as e:
        print(f"An unexpected error occurred during bot execution: {e}")
