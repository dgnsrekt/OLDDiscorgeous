import asyncore
import sys
from voice_message import VoiceMessageFile, VoiceMessageQueue
from threading import Thread
from time import sleep


class DiscordGttsHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(4096)  # add to config
        data = data.decode().replace('\n', '').replace('\r', '')
        print(f'found: {data}')
        print(f'len: {len(data)}')
        if data:
            self.send(b'ACK!\n')
            VoiceMessageQueue.push(data)


class DiscordGttsServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(10)  # add to config
        print(f'Listing on {host} {port}')

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = DiscordGttsHandler(sock)


def worker():
    vmf = VoiceMessageFile()
    while True:
        if not vmf.file_exists:
            msg = VoiceMessageQueue.pop()
            vmf.create_message(msg)  # logging here
        sleep(1)


if __name__ == '__main__':
    server = DiscordGttsServer('localhost', 6666)
    t = Thread(target=worker)
    try:
        t.start()
        asyncore.loop()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
