from requests_html import HTMLSession
from time import sleep
from client import DiscorGttsClient
import requests
from random import randint


session = HTMLSession()
url = 'http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1&callback='


def get_quote():
    while True:
        resp = session.get(url)
        if resp.status_code == requests.codes.ok:
            yield resp.json()[0]['content'].replace('<p>', '').replace('</p>', '').replace('&#8217;', "'")


client = DiscorGttsClient('0.0.0.0', 6666)

rand = randint(1, 25)
print(rand)
for i, x in enumerate(get_quote()):
    client.send_voice_msg(x)
    if i == rand:
        break
