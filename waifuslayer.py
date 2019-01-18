# Work with Python 3.6
import random
import re
import asyncio
import aiohttp
import json
import cv2
import sys
import os
import os.path
from urllib.request import Request, urlopen
import uuid
from discord import Game
from discord.ext.commands import Bot

# !!!!!!!!!!!!!!!!!!!!!!!!README!!!!!!!!!!!!!!!!!!!!!!!!
# Account token must be stored in a file called 'account.token'
TOKEN = file_contents("account.token").strip()

print("===============================================")
print("            STARTING WAIFU SLAYER!             ")
print("===============================================")

BOT_PREFIX = ("?", "!")
x = (" ")
client = Bot(command_prefix=BOT_PREFIX)

@client.command(name = 'Purge?',
    description = "Answers the question, is it time to purge?",
    brief = "Answers from the beyond.",
    aliases = ['purge', 'Purge', 'purge?'],
    pass_context = True)
async def eight_ball(context):
    possible_responses = [
        'Let us kill all those who oppose the Enclave',
        'Death to anime',
        'The command has not yet given the order',
        'It is time to kill mutie scum',
        'We will purge the the land of the impure',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))

@client.event
async def on_ready():
    #await client.change_presence(game = Game(name = "a Vertibird Simulator"))
    print("LOGGED IN AS '" + client.user.name + "'")

@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session: #Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("CURRENT SERVERS:")
        for server in client.servers:
            print(" - " + server.name)
        
        possible_game_names = [
            "a Vertibird Simulator", "Waifu Execution Simulator", "Waifu Hunter III"]
        choice = random.choice(possible_game_names)
        print("CHANGED PRESENCE TO '" + choice + "'")
        await client.change_presence(game = Game(name = choice))
        await asyncio.sleep(600)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    reduced = message.content.lower().replace(' ', '').replace('\n', '')
    triggers = ['anime', 'anlme', 'amine', 'ƒnÔmÎ']
    found_anime = False
    for trigger in triggers:
        if trigger in reduced:
            found_anime = True
            break
    for attachment in message.attachments:
        print("GOT URL " + attachment["proxy_url"])
        filename = str(uuid.uuid4()) + os.path.splitext(attachment["proxy_url"])[-1]
        request = Request(attachment["proxy_url"], headers={'User-Agent': 'Mozilla/5.0'})
        f = open(filename, 'wb')
        f.write(urlopen(request).read())
        f.close()
        if detect(filename) > 0:
            await client.send_message(message.channel, "That is anime")
            found_anime = True
        # else:
            # await client.send_message(message.channel, "That is not anime")
        os.remove(filename)
    if found_anime:
        possible_messages = [
            'No anime allowed mutie scum, {0.author.mention}'.format(message)
        ]
        await client.send_message(message.channel, random.choice(possible_messages))
        await client.delete_message(message)

def detect(filename, cascade_file = "lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)
    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.equalizeHist(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    faces = cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (24, 24))
    return len(faces)

def file_contents(filename):
    with open(filename) as f:
        return f.read()

client.loop.create_task(list_servers())
client.run(TOKEN)
