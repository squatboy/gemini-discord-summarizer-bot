import discord
import datetime
from config import MESSAGE_FETCH_LIMIT


async def fetch_messages(
    channel: discord.TextChannel,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    bot_user: discord.ClientUser,
    command_prefix: str,
) -> tuple[str, int]:
    """주어진 시간 범위 내의 채널 메시지를 가져와 하나의 문자열로 만듭니다."""
    messages_content = []
    message_count = 0
    fetched_count = 0
    print(
        f"'{channel.name}' 채널 메시지 가져오기 시작: {start_time.isoformat()} ~ {end_time.isoformat()}"
    )

    try:
        async for message in channel.history(
            limit=MESSAGE_FETCH_LIMIT,
            after=start_time,
            before=end_time,
            oldest_first=True,
        ):
            fetched_count += 1
            # 봇 자신의 메시지, 다른 봇 메시지, 명령어 메시지는 제외
            if (
                message.author == bot_user
                or message.author.bot
                or message.content.startswith(command_prefix)
            ):
                continue

            # 간단한 형식으로 메시지 내용 저장 (작성자: 내용)
            messages_content.append(f"{message.author.display_name}: {message.content}")
            message_count += 1

        print(f"총 {fetched_count}개 메시지 확인, 요약 대상 {message_count}개.")

        if not messages_content:
            return "", 0  # 요약할 메시지 없음

        # 모든 메시지를 하나의 문자열로 결합
        full_text = "\n".join(messages_content)
        return full_text, message_count

    except discord.Forbidden:
        print(f"오류: 채널 '{channel.name}'의 메시지 기록 접근 권한이 없습니다.")
        raise  # 오류를 다시 발생시켜 호출한 곳에서 처리하도록 함
    except Exception as e:
        print(f"메시지 수집 중 오류 발생: {e}")
        raise  # 오류를 다시 발생시켜 호출한 곳에서 처리하도록 함


async def send_long_message(
    channel: discord.TextChannel, content: str, prefix: str = ""
):
    """긴 메시지를 Discord 제한에 맞게 나누어 전송합니다."""
    max_len = 1950  # 약간의 여유를 둠
    start_index = 0
    first_message = True

    while start_index < len(content):
        end_index = start_index + max_len
        # 줄바꿈 기준으로 자르기 시도
        last_newline = content.rfind("\n", start_index, end_index)
        if last_newline > start_index and end_index < len(
            content
        ):  # 중간에 있고, 마지막 조각이 아니면
            end_index = last_newline + 1  # 줄바꿈 문자 포함하여 자름

        part = content[start_index:end_index]

        if first_message and prefix:
            await channel.send(f"> ## 📝 {prefix}\n{part}")
            first_message = False
        else:
            await channel.send(part)

        start_index = end_index
