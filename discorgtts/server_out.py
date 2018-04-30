import asyncio
import io
import os

import discord
from config import load_config_file
from voice_message import VoiceMessage

config = load_config_file()['server']
print(config)
channel_id = config['channel_id']
token = config['discord_voice_token']
message = VoiceMessage()

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')


async def on_ready():
    await client.wait_until_ready()

    channel = discord.Object(id=channel_id)
    voice = await client.join_voice_channel(channel)

    start_time = message.mtime
    print(f'file start: {start_time}')

    while True:
        updated_time = message.mtime
        if updated_time > start_time:
            start_time = updated_time
            player = voice.create_ffmpeg_player(message.file)
            player.start()
            while not player.is_done():
                await asyncio.sleep(message.duration)
        await asyncio.sleep(1)

if __name__ == '__main__':
    client = discord.Client()
    client.loop.create_task(on_ready())
    client.run(token)
