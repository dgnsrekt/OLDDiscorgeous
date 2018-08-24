# TODO: MOVE TO EXAMPLE FOLDER
from time import sleep

from client import DiscorGttsClient

client = DiscorGttsClient('0.0.0.0', 6666)

# for message in test_messages:
# print(message)
# client.send_voice_msg(message)
# sleep(5)

while True:
    client.send_voice_msg('test')
    sleep(3.25)
