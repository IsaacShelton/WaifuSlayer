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
from discord.ext import commands
from discord.ext.commands import Bot

# !!!!!!!!!!!!!!!!!!!!!!!!README!!!!!!!!!!!!!!!!!!!!!!!!
# Account token must be stored in a file called 'account.token'
with open('account.token') as f:
    TOKEN = f.read()

print("===============================================")
print("            STARTING WAIFU SLAYER!             ")
print("===============================================")

BOT_PREFIX = ("?", "!")
x = (" ")
client = Bot(command_prefix="!")

@client.command(name = 'Waifu?',
    description = "Answers the question, is it time to purge?",
    brief = "Answers from the beyond.",
    aliases = ['purge', 'Purge', 'purge?'],
    pass_context = True)
async def eight_ball(context):
    possible_responses = [
        'It could be certain!',
        'I am the only Waifu!',
        'Death to the false idols! :heart:',
        'It is time to kill the false Waifus!',
        'We will purge the the land of the impure :(',
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
            "a Waifu Slayer Simulation",
            "Waifu Execution Simulator",
            "Waifu Hunter III",
            "Heart Breaker 2",
            "Don't Kill Blonde Lucina <3",
            "<3"
        ]
        choice = random.choice(possible_game_names)
        print("CHANGED PRESENCE TO '" + choice + "'")
        await client.change_presence(game = Game(name = choice))
        await asyncio.sleep(600)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    found_anime = False
    if re.search(r'[aA]+\s*[nN]+\s*[iILl\|]+\s*[mM]+\s*[eE]', message.content):
        found_anime = True
    for attachment in message.attachments:
        print("GOT URL " + attachment["proxy_url"])
        filename = str(uuid.uuid4()) + os.path.splitext(attachment["proxy_url"])[-1]
        request = Request(attachment["proxy_url"], headers={'User-Agent': 'Mozilla/5.0'})
        f = open(filename, 'wb')
        f.write(urlopen(request).read())
        f.close()
        if detect(filename) > 0:
            await client.send_message(message.channel, "That is a false Waifu!")
            found_anime = True
        # else:
            # await client.send_message(message.channel, "That is not anime")
        os.remove(filename)
    if found_anime:
        possible_messages = [
            'no false waifus allowed mister, {0.author.mention}! :broken_heart:'.format(message),
            'your waifus are not permited here mister, {0.author.mention}! :broken_heart:'.format(message),
            'no anime allowed mister, {0.author.mention}! :broken_heart:'.format(message),
            'wow your waifu is ugly {0.author.mention}! :broken_heart:'.format(message),
            'heehee! only blonde lucina is allowed {0.author.mention}! :broken_heart:'.format(message),
            'lol, {0.author.mention} is a filthy weeb! :broken_heart:'.format(message),
            'inferior waifu detected! no inferior waifus allowed {0.author.mention}! :broken_heart:'.format(message),
        ]
        choice = random.choice(possible_messages)
        if 'lucina' in choice:
            possible_images = ['1.png', '2.png']
            await client.send_file(message.channel, 'betterthanbestwaifu/' + random.choice(possible_images))
        await client.send_message(message.channel, choice)
        await client.delete_message(message)

def detect(filename, cascade_file = "lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)
    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.equalizeHist(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    faces = cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (24, 24))
    return len(faces)

client.loop.create_task(list_servers())
client.run(TOKEN)
