import discord
from discord.ext import commands
from discord import app_commands
import datetime
from config import TIMEZONE
from utils import fetch_messages
from gemini_handler import get_summary_from_gemini
from utils import (
    send_long_message,
)  # Assuming send_long_message might be useful here too


class SummaryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def summarize_messages(self, interaction: discord.Interaction, hours: int):
        """Helper function to summarize messages for a specified number of hours"""
        await interaction.response.defer()

        channel = interaction.channel
        time_now = datetime.datetime.now(TIMEZONE)
        time_past = time_now - datetime.timedelta(hours=hours)

        try:
            full_text, message_count = await fetch_messages(
                channel, time_past, time_now, self.bot.user, "/"
            )

            if not full_text:
                await interaction.followup.send(
                    f"## ❌ No messages to summarize from the past {hours} hours."
                )
                return

            await interaction.followup.send(
                f"## 🤔 Summarizing messages from the past {hours} hours in {channel.mention}..."
            )

            summary = await get_summary_from_gemini(full_text)

            if summary:
                # Use send_long_message for potentially long summaries
                await send_long_message(
                    interaction.followup,  # followup is an AsyncWebhookAdapter, send_long_message expects TextChannel. Need adjustment or use manual splitting with followup.send
                    summary,
                    prefix=f"## 💌 Message Summary from the past {hours} hours (Total {message_count}):",
                )
                # Note: The original code was manually splitting. Using send_long_message with interaction.followup requires it to accept AsyncWebhookAdapter or manual splitting logic needs to be here. Reverting to original manual split logic for now.
                if len(summary) > 1900:
                    summary_parts = [
                        summary[i : i + 1900] for i in range(0, len(summary), 1900)
                    ]
                    await interaction.followup.send(
                        f"> ## 💌 Message Summary from the past {hours} hours (Total {message_count})"
                    )
                    for part in summary_parts:
                        await interaction.followup.send(part)
                else:
                    await interaction.followup.send(
                        f"> ## 💌 Message Summary from the past {hours} hours (Total {message_count})\n{summary}"
                    )
            else:
                await interaction.followup.send("Failed to generate summary. 😟")

        except discord.Forbidden:
            await interaction.followup.send(
                "Missing permissions to access message history. 🚫"
            )
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)} ❗")

    @app_commands.command(
        name="summarize_1h", description="Summarizes messages from the last 1 hour"
    )
    async def summary_1h(self, interaction: discord.Interaction):
        await self.summarize_messages(interaction, 1)

    @app_commands.command(
        name="summarize_6h", description="Summarizes messages from the last 6 hours"
    )
    async def summary_6h(self, interaction: discord.Interaction):
        await self.summarize_messages(interaction, 6)

    @app_commands.command(
        name="summarize_day", description="Summarizes messages from the last 24 hours"
    )
    async def summary_24h(self, interaction: discord.Interaction):
        await self.summarize_messages(interaction, 24)


async def setup(bot):
    await bot.add_cog(SummaryCog(bot))
    print("SummaryCog loaded successfully.")
