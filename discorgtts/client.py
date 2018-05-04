import os
import socket

from time import sleep

import logging as log


class DiscorGttsClient:
    def __init__(self, bind_ip, bind_port, sleep_time=0.5, byte_chunks=4096):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.sleep_time = sleep_time
        self.byte_chunks = byte_chunks

    def send_voice_msg(self, message):

        assert isinstance(message, str), 'Message must be type string.'
        assert len(message) >= 1, 'Message can not be empty.'

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self.bind_ip, self.bind_port))
            sleep(self.sleep_time)

            client.send(message.encode())
            response = client.recv(self.byte_chunks)

            if response:
                log.info('message sent.')
            else:
                log.error('message not acknowledged.')  # may need a higher logg type

        except ConnectionRefusedError:
            log.error('Server may not be running meesage not sent.')
        except ConnectionResetError as e:
            log.error(e)
            raise  # catch em all
        finally:
            client.close()


class DiscordGttsSSHClient(DiscorGttsClient):
    pass
