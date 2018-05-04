import asyncore
import sys

from config import Configuration
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
            print(data)
            VoiceMessageQueue.push(data)


class DiscordGttsServer(asyncore.dispatcher):  # TODO: Change to DiscordGttsInput

    def __init__(self, host, port, max_conn=10):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(max_conn)  # add to config
        log.info(f'Listing on {host} {port}')

    def handle_accepted(self, sock, addr):
        log.info('Incoming connection from %s' % repr(addr))
        handler = DiscordGttsHandler(sock)


class DiscordGttsServerInput:  # TODO: Change to DiscordGttsInputServer

    def __init__(self, ip, port, language, max_connections):
        self.server = DiscordGttsServer(ip, port, max_connections)
        self.worker = Thread(target=self.start_voice_messsage_queue)  # TODO change this to async
        self.worker2 = Thread(target=asyncore.loop, name='Asyncore Loop')
        self.language = language

    def start_voice_messsage_queue(self):
        vmf = VoiceMessageFile()
        while True:
            if not vmf.file_exists:
                message = VoiceMessageQueue.pop()
                vmf.create_message(message, self.language)  # logging here
            sleep(1)  # try .5 for speed

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

    config = Configuration()
    bind_ip = config.server_settings['server_ip']
    bind_port = int(config.server_settings['server_port'])
    language = config.server_settings['language']
    max_connections = int(config.server_settings['max_connections'])

    server = DiscordGttsServerInput(bind_ip, bind_port, language, max_connections)
    server.run()


if __name__ == '__main__':
    main()
