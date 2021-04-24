import discord
from discord.ext import commands
import requests

TOKEN = "ODM0NDU3MDY2NzQ3NDYxNjMz.YIBKtA.zmxaOKi87Bn4k1zjoRCeJUYKkpE"

client = commands.Bot(command_prefix='mb!')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="mb! help"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    s = message.content.split()

    if s[0] == 'mb!':
        if s[1].lower() == 'getmemeuser':
            q = f'http://127.0.0.1:5000/export/{s[2]}/{s[3]}'
            request = requests.get(q)
            if request:
                answ = 'http://127.0.0.1:5000/static/' + requests.get(q).json()
                await message.channel.send(answ)
            else:
                await message.channel.send('Error in image getting')
                await message.channel.send(s)
        elif s[1] == 'getmemepublic':
            await message.chanel.send('WIP')
        elif s[1] == 'help':
            await message.chanel.send('getmemeuser <username> <key> to get your meme')
            await message.chanel.send('getmemepublic <key> to get a public meme')


    # if 'mb!' in message.content.lower()[0:3]:
    #     if ' getmeme' in message.content.lower()[3:11]:
    #         q = 'https://flaskprojstud.herokuapp.com/export/' + message.content[12:]
    #         request = requests.get(q)
    #         if request:
    #             answ = 'https://flaskprojstud.herokuapp.com/static/' + requests.get(q).json()
    #         else:
    #             answ = 'Error in image getting'
    #     else:
    #         answ = 'repy'
    # try:
    #     await message.channel.send(answ)
    # except Exception:
    #     pass

client.run(TOKEN)
