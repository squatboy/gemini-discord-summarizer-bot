import discord
from discord.ext import commands, tasks
import datetime
from config import TARGET_CHANNEL_ID, TIMEZONE
from gemini_handler import get_summary_from_gemini
from utils import fetch_messages, send_long_message


class SchedulerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel_id = TARGET_CHANNEL_ID
        self.timezone = TIMEZONE
        self.daily_summary.start()  # Start the scheduler when the Cog is loaded

    def cog_unload(self):
        self.daily_summary.cancel()  # Stop the scheduler when the Cog is unloaded

    @tasks.loop(
        time=datetime.time(hour=0, minute=0, second=0, tzinfo=TIMEZONE)
    )  # Midnight in the configured timezone
    async def daily_summary(self):
        """Summarizes messages from the previous day in the specified channel at midnight."""
        await self.bot.wait_until_ready()  # Wait until the bot is ready

        channel = self.bot.get_channel(self.target_channel_id)
        if not channel or not isinstance(channel, discord.TextChannel):
            print(
                f"Error: Target channel ID ({self.target_channel_id}) not found or is not a text channel. ❌"
            )
            return

        # Calculate yesterday's date (based on the configured timezone)
        now_local = datetime.datetime.now(TIMEZONE)
        yesterday_end = now_local.replace(
            hour=0, minute=0, second=0, microsecond=0
        )  # Today's midnight = End of yesterday
        yesterday_start = yesterday_end - datetime.timedelta(
            days=1
        )  # Start of yesterday

        print(
            f"Starting automatic daily summary: Channel '{channel.name}', Time range: {yesterday_start.isoformat()} ~ {yesterday_end.isoformat()}"
        )

        try:
            await channel.send(
                f"## 📅 Starting automatic message summary for {yesterday_start.strftime('%Y-%m-%d')}..."
            )

            # Fetch messages (convert to UTC for comparison - Discord API uses UTC)
            start_utc = yesterday_start.astimezone(datetime.timezone.utc)
            end_utc = yesterday_end.astimezone(datetime.timezone.utc)
            full_text, message_count = await fetch_messages(
                channel,
                start_utc,
                end_utc,
                self.bot.user,
                self.bot.command_prefix,  # Pass command prefix
            )

            if not full_text:
                await channel.send("# No messages to summarize from yesterday. 🤷")
                print("Automatic summary: No messages to summarize.")
                return

            # Request Gemini summary
            summary = await get_summary_from_gemini(full_text)

            if summary:
                await send_long_message(
                    channel,
                    summary,
                    prefix=f"## {yesterday_start.strftime('%Y-%m-%d')} Message Summary (Total {message_count}):",
                )
                print(f"Automatic summary completed for channel: '{channel.name}'")
            else:
                await channel.send(
                    "## Failed to generate summary for yesterday's messages. 😟"
                )
                print("Automatic summary: Failed to generate summary.")

        except discord.Forbidden:
            print(
                f"Error: Missing permissions to access message history in channel '{channel.name}' (automatic summary) 🚫"
            )
            # Log only, as sending a message might also fail due to permissions
        except Exception as e:
            print(f"An error occurred during automatic daily summary: {e}")
            try:
                await channel.send(
                    f"An error occurred during automatic summary execution: {e}"
                )
            except Exception as send_error:
                print(f"Failed to send error message: {send_error}")

    @daily_summary.before_loop
    async def before_daily_summary(self):
        print("Automatic summary scheduler: Waiting for the bot to be ready...")
        await self.bot.wait_until_ready()
        print("Automatic summary scheduler: Bot ready, waiting to start loop.")


async def setup(bot):
    await bot.add_cog(SchedulerCog(bot))
    print("SchedulerCog loaded successfully.")
