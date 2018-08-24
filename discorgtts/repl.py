from client import DiscorGttsClient
from prompt_toolkit import prompt
from time import sleep

client = DiscorGttsClient('0.0.0.0', 6666)

while True:
    try:
        message = prompt(':>')
        client.send_voice_msg(message)
    except AssertionError:
        pass
