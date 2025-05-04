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
        self.daily_summary.start()  # Cog 로드 시 스케줄러 시작

    def cog_unload(self):
        self.daily_summary.cancel()  # Cog 언로드 시 스케줄러 중지

    @tasks.loop(
        time=datetime.time(hour=0, minute=0, second=0, tzinfo=TIMEZONE)
    )  # 설정된 시간대의 자정
    async def daily_summary(self):
        """매일 자정에 지정된 채널의 이전 하루 메시지를 요약합니다."""
        await self.bot.wait_until_ready()  # 봇이 준비될 때까지 기다림

        channel = self.bot.get_channel(self.target_channel_id)
        if not channel or not isinstance(channel, discord.TextChannel):
            print(
                f"오류: 대상 채널 ID ({self.target_channel_id})를 찾을 수 없거나 텍스트 채널이 아닙니다."
            )
            return

        # 어제 날짜 계산 (설정된 시간대 기준)
        now_local = datetime.datetime.now(TIMEZONE)
        yesterday_end = now_local.replace(
            hour=0, minute=0, second=0, microsecond=0
        )  # 오늘 자정 = 어제 끝
        yesterday_start = yesterday_end - datetime.timedelta(days=1)  # 어제 시작

        print(
            f"자동 일일 요약 시작: 채널 '{channel.name}', 시간 범위: {yesterday_start.isoformat()} ~ {yesterday_end.isoformat()}"
        )

        try:
            await channel.send(
                f"## 📅 {yesterday_start.strftime('%Y년 %m월 %d일')} 메시지 자동 요약을 시작합니다..."
            )

            # 메시지 가져오기 (UTC로 변환하여 비교 - Discord API는 UTC 사용)
            start_utc = yesterday_start.astimezone(datetime.timezone.utc)
            end_utc = yesterday_end.astimezone(datetime.timezone.utc)
            full_text, message_count = await fetch_messages(
                channel,
                start_utc,
                end_utc,
                self.bot.user,
                self.bot.command_prefix,  # 명령어 접두사 전달
            )

            if not full_text:
                await channel.send("# 어제는 요약할 메시지가 없었습니다.")
                print("자동 요약: 요약할 메시지 없음.")
                return

            # Gemini 요약 요청
            summary = await get_summary_from_gemini(full_text)

            if summary:
                await send_long_message(
                    channel,
                    summary,
                    prefix=f"## {yesterday_start.strftime('%Y년 %m월 %d일')} 메시지 요약 (총 {message_count}개):",
                )
                print(f"자동 요약 완료: '{channel.name}' 채널")
            else:
                await channel.send("## 어제 메시지 요약 생성에 실패했습니다.")
                print("자동 요약: 요약 생성 실패.")

        except discord.Forbidden:
            print(
                f"오류: 채널 '{channel.name}'의 메시지 기록 접근 권한 부족 (자동 요약)"
            )
            # 채널에 알림을 보내려 해도 권한이 없을 수 있으므로 로그만 남김
        except Exception as e:
            print(f"자동 일일 요약 중 오류 발생: {e}")
            try:
                await channel.send(f"자동 요약 실행 중 오류가 발생했습니다: {e}")
            except Exception as send_error:
                print(f"오류 메시지 전송 실패: {send_error}")

    @daily_summary.before_loop
    async def before_daily_summary(self):
        print("자동 요약 스케줄러: 봇이 준비되기를 기다리는 중...")
        await self.bot.wait_until_ready()
        print("자동 요약 스케줄러: 봇 준비 완료, 루프 시작 대기.")


async def setup(bot):
    await bot.add_cog(SchedulerCog(bot))
    print("SchedulerCog 로드 완료.")
