import asyncore
from voice_message import VoiceMessage


class DiscordGttsHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        self.dispatcher = VoiceMessage()
        if len(data) > 2:
            self.send(b'ACK!\n')
            self.dispatcher.generate_gtts(data.decode())


class DiscordGttsServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)  # was 5
        print(f'Listing on {host} {port}')

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = DiscordGttsHandler(sock)


if __name__ == '__main__':
    server = DiscordGttsServer('localhost', 6666)
    asyncore.loop()
