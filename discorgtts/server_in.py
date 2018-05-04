# TODO: Rename file DiscordGttsServerInput
# TODO: Convert to ASYNCIO
# https://docs.python.org/3/library/asyncio-protocol.html#udp-echo-server-protocol -> 18.5.4.3.2. TCP echo server protocol
import asyncore
import sys
from voice_message import VoiceMessageFile, VoiceMessageQueue
from threading import Thread
from time import sleep

import logging as log


class DiscordGttsHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(4096)  # add to config
        data = data.decode().replace('\n', '').replace('\r', '')
        log.info(f'found: {data}')
        log.info(f'len: {len(data)}')
        if data:
            self.send(b'ACK!\n')
            VoiceMessageQueue.push(data)


class DiscordGttsServer(asyncore.dispatcher):  # TODO: Change to DiscordGttsInput

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(10)  # add to config
        log.info(f'Listing on {host} {port}')

    def handle_accepted(self, sock, addr):
        log.info('Incoming connection from %s' % repr(addr))
        handler = DiscordGttsHandler(sock)


class DiscordGttsServerInput:  # TODO: Change to DiscordGttsInputServer

    def __init__(self):
        self.server = DiscordGttsServer('localhost', 6666)
        self.worker = Thread(target=self.start_voice_messsage_queue)  # TODO change this to async
        self.worker2 = Thread(target=asyncore.loop, name='Asyncore Loop')
        self.stop_queue = False

    def start_voice_messsage_queue(self):
        vmf = VoiceMessageFile()
        while True:
            if not vmf.file_exists:
                message = VoiceMessageQueue.pop()
                vmf.create_message(message)  # logging here
            sleep(1)  # try .5 for speed
        return

    def run(self):
        try:
            self.worker.start()
            self.worker2.start()
        except (KeyboardInterrupt, SystemExit):
            self.worker.join()
            self.worker2.join()
            sys.exit()


def main():
    sleep(1)
    print('running input server')
    server = DiscordGttsServerInput()
    server.run()


if __name__ == '__main__':
    main()
