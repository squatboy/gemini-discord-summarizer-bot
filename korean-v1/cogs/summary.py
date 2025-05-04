import discord
from discord.ext import commands
from discord import app_commands
import datetime
from config import TIMEZONE
from utils import fetch_messages
from gemini_handler import get_summary_from_gemini


class SummaryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def summarize_messages(self, interaction: discord.Interaction, hours: int):
        """지정된 시간 동안의 메시지를 요약하는 헬퍼 함수"""
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
                    f"## ❌ 지난 {hours}시간 동안 요약할 메시지가 없습니다."
                )
                return

            await interaction.followup.send(
                f"## 🤔 {channel.mention} 채널의 지난 {hours}시간 메시지를 요약하고 있어요..."
            )

            summary = await get_summary_from_gemini(full_text)

            if summary:
                if len(summary) > 1900:
                    summary_parts = [
                        summary[i : i + 1900] for i in range(0, len(summary), 1900)
                    ]
                    await interaction.followup.send(
                        f"> ## 💌 지난 {hours}시간 메시지 요약 (총 {message_count}개)"
                    )
                    for part in summary_parts:
                        await interaction.followup.send(part)
                else:
                    await interaction.followup.send(
                        f"> ## 💌 지난 {hours}시간 메시지 요약 (총 {message_count}개)\n{summary}"
                    )
            else:
                await interaction.followup.send("요약 생성에 실패했습니다.")

        except discord.Forbidden:
            await interaction.followup.send("메시지 기록 접근 권한이 없습니다.")
        except Exception as e:
            await interaction.followup.send(f"오류가 발생했습니다: {str(e)}")

    @app_commands.command(
        name="요약_1시간", description="최근 1시간의 메시지를 요약합니다"
    )
    async def summary_1h(self, interaction: discord.Interaction):
        await self.summarize_messages(interaction, 1)

    @app_commands.command(
        name="요약_6시간", description="최근 6시간의 메시지를 요약합니다"
    )
    async def summary_6h(self, interaction: discord.Interaction):
        await self.summarize_messages(interaction, 6)

    @app_commands.command(
        name="요약_하루", description="최근 24시간의 메시지를 요약합니다"
    )
    async def summary_24h(self, interaction: discord.Interaction):
        await self.summarize_messages(interaction, 24)


async def setup(bot):
    await bot.add_cog(SummaryCog(bot))
    print("SummaryCog 로드 완료.")
