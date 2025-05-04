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
    """Fetches channel messages within a given time range and combines them into a single string."""
    messages_content = []
    message_count = 0
    fetched_count = 0
    print(
        f"Starting to fetch messages in channel '{channel.name}': {start_time.isoformat()} ~ {end_time.isoformat()}"
    )

    try:
        async for message in channel.history(
            limit=MESSAGE_FETCH_LIMIT,
            after=start_time,
            before=end_time,
            oldest_first=True,
        ):
            fetched_count += 1
            # Exclude bot's own messages, other bot messages, and command messages
            if (
                message.author == bot_user
                or message.author.bot
                or message.content.startswith(command_prefix)
            ):
                continue

            # Store message content in a simple format (Author: Content)
            messages_content.append(f"{message.author.display_name}: {message.content}")
            message_count += 1

        print(
            f"Total messages checked: {fetched_count}, Messages for summary: {message_count}."
        )

        if not messages_content:
            return "", 0  # No messages to summarize

        # Combine all messages into a single string
        full_text = "\n".join(messages_content)
        return full_text, message_count

    except discord.Forbidden:
        print(
            f"Error: Missing permissions to access message history in channel '{channel.name}'. 🚫"
        )
        raise  # Re-raise the error for handling by the caller
    except Exception as e:
        print(f"Error occurred while collecting messages: {e}")
        raise  # Re-raise the error for handling by the caller


async def send_long_message(
    channel: discord.TextChannel, content: str, prefix: str = ""
):
    """Sends a long message split according to Discord limits."""
    max_len = 1950  # Leave some buffer
    start_index = 0
    first_message = True

    while start_index < len(content):
        end_index = start_index + max_len
        # Try to split by newline
        last_newline = content.rfind("\n", start_index, end_index)
        if last_newline > start_index and end_index < len(
            content
        ):  # If in the middle and not the last part
            end_index = last_newline + 1  # Include the newline character

        part = content[start_index:end_index]

        if first_message and prefix:
            await channel.send(f"> ## 📝 {prefix}\n{part}")
            first_message = False
        else:
            await channel.send(part)

        start_index = end_index
