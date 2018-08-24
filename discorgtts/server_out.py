# TODO: Rename file DiscordGttsServerOuput

import asyncio
import io
import os

import discord
from config import Configuration
from filelock import Timeout

from voice_message import VoiceMessageFile
from time import time, sleep

import logging as log


if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')


class DiscordGttsServerOutput:  # TODO: Change to DiscordGttsOuput Server
    def __init__(self, token,  channel_id, sample_rate=48000,
                 audio_channel=1, sleep_time=.1):

        self.token = token
        self.channel_id = channel_id
        self.sample_rate = sample_rate
        self.audio_channel = audio_channel

        self.sleep_time = sleep_time  # .75

        self.vmf = VoiceMessageFile()
        self.client = discord.Client()

    async def on_ready(self):
        await self.client.wait_until_ready()

        channel = discord.Object(id=self.channel_id)
        voice = await self.client.join_voice_channel(channel)
        voice.encoder_options(sample_rate=self.sample_rate, channels=self.audio_channel)

        start_time = time()
        self.vmf.remove()  # deletes message file
        log.info(f'Server Start Time: {start_time}')

        while True:
            if self.vmf.file_exists:
                updated_time = self.vmf.mtime
                # await asyncio.sleep(self.sleep_time)

                if updated_time > start_time:
                    print(start_time)
                    print(updated_time)
                    start_time = updated_time
                    print(start_time)

                    # while file is locked wiath .01 else create and start
                    while True:
                        try:
                            self.vmf.filelock.acquire()
                            print('lock aquired')
                            player = voice.create_ffmpeg_player(self.vmf.file)
                            player.start()

                            break
                        except Timeout:
                            print('.', end='', flush=True)
                            sleep(.01)
                            await asyncio.sleep(.01)
                        finally:
                            self.vmf.filelock.release()

                    while not player.is_done():
                        await asyncio.sleep(.01)
                        print('.', end='', flush=True)

                    else:
                        print('done')
                        player.stop()
                        await asyncio.sleep(.01)
                        self.vmf.remove()
                        print('deleted')

                # if player.is_done():
                    # player.stop()
                    # self.vmf.remove()
                    # print('deleted')

                if player.error:
                    print('error')
                    print(player.error)

                # if player.is_playing() == False:
                    # player.stop()
                    # self.vmf.remove()
                    # print('deleted2')

            # await asyncio.sleep(self.sleep_time)

    def run(self):
        self.client.loop.create_task(self.on_ready())
        self.client.run(self.token)


def main():
    sleep(1)
    print('running output server')
    config = Configuration()

    token = config.server_settings['discord_voice_token']
    channel_id = config.server_settings['channel_id']
    sample_rate = config.server_settings['encoder_sample_rate']
    encoder_channel_rate = config.server_settings['encoder_channel']

    server = DiscordGttsServerOutput(token, channel_id)
    server.run()


if __name__ == '__main__':
    main()
