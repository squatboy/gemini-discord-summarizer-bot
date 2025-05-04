import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
from config import DISCORD_TOKEN

# Discord 봇 설정
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True


class SummaryBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("슬래시 커맨드 동기화 완료!")


bot = SummaryBot()


@bot.event
async def on_ready():
    """봇이 준비되었을 때 실행되는 이벤트"""
    print(f"로그인: {bot.user.name} (ID: {bot.user.id})")
    print(f"discord.py 버전: {discord.__version__}")
    print("------")
    await bot.change_presence(activity=discord.Game(name="/요약 | 대화 요약"))


async def load_extensions():
    """cogs 폴더 안의 모든 Cog를 로드합니다."""
    cogs_path = "cogs"
    for filename in os.listdir(cogs_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            try:
                # 파일 경로를 모듈 경로 형태로 변환 (e.g., cogs/summary.py -> cogs.summary)
                await bot.load_extension(f"{cogs_path}.{filename[:-3]}")
            except Exception as e:
                print(f"{filename[:-3]} Cog 로딩 실패.")
                print(f"[오류] {e}")


async def main():
    """봇을 시작하고 Cog를 로드합니다."""
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("봇 종료 중...")
    except ValueError as e:  # config.py에서 발생시킨 오류 처리
        print(f"설정 오류: {e}")
    except discord.LoginFailure:
        print(
            "Discord 로그인 실패: 잘못된 토큰이거나 네트워크 문제가 있을 수 있습니다."
        )
    except Exception as e:
        print(f"봇 실행 중 예기치 않은 오류 발생: {e}")
