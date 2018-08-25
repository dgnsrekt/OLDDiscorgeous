# TODO: MOVE TO EXAMPLE FOLDER
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


def quoteforce():
    rand = randint(1, 25)
    print(rand)
    quotes = list()
    for i, x in enumerate(get_quote()):
        quotes.append(x)
        if i == rand:
            break
    return quotes


text1 = list('12345678910')
text2 = list('abcdefghijklmnopqrstuvwxyz')
text3 = """This was a triumph!
I'm making a note here Huge success!

It's hard to overstate my satisfaction.

At Fomo D D: We do what we must
because we can for the good of all of us.
Except the ones who are dead.

But there's no sense crying over every mistake.
You just keep on trying 'til you run out of cake.
And the science gets done.
And you make a neat gun for the people who are still alive.

I'm not even angry... I'm being so sincere right now.
Even though you broke my heart, and killed me.

And tore me to pieces.
And threw every piece into a fire.
As they burned it hurt because I was so happy for you!

Now, these points of data make a beautiful line.
And we're out of beta.
We're releasing on time!
So I'm GLaD I got burned!
Think of all the things we learned!
for the people who are still alive.

Go ahead and leave me...
I think I'd prefer to stay inside...
Maybe you'll find someone else to help you.
Maybe Black Mesa?
That was a joke. Ha Ha. Fat Chance!

Anyway this cake is great!
It's so delicious and moist!

Look at me: still talking
when there's science to do!
When I look out there,
it makes me glad I'm not you.

I've experiments to run.
There is research to be done.
On the people who are still alive.
And believe me I am still alive.
I'm doing science and I'm still alive.
I feel fantastic and I'm still alive.
While you're dying I'll be still alive.
And when you're dead I will be still alive

Still alive.

Still alive.""".split('\n')
text4 = quoteforce()
test_messages = text4 + text3 + text2 + text1
test_messages = list(filter(None, test_messages))  # filter out empty str

client = DiscorGttsClient('0.0.0.0', 6666)


def bruteforce(n):
    for message in test_messages:
        print(message)
        client.send_voice_msg(message)
        sleep(n)


while True:
    for i in range(5, 0, -1):
        bruteforce(i)
    else:
        sleep(30)
