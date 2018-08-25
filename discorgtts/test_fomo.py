# TODO: MOVE TO EXAMPLE FOLDER
from time import sleep

from client import DiscorGttsClient
from pathlib import Path
import sys
from time import sleep

import requests


def get_coins():
    url = 'https://api.fomodd.io/superfilter'
    r = requests.get(url)
    data = r.json()
    binance = data['BINANCE']['coins']
    # binance = [f'BINANCE:{coin}' for coin in binance]
    bittrex = data['BITTREX']['coins']
    # bittrex = [f'BITTREX:{coin}' for coin in bittrex]

    coins = binance + bittrex
    return coins


client = DiscorGttsClient('0.0.0.0', 6666)

# for message in test_messages:
# print(message)
# client.send_voice_msg(message)
# sleep(5)

for coin in get_coins():
    print(coin)
    client.send_voice_msg(f'found {coin}')
