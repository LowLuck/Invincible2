import discord
from discord.ext import commands
import requests

TOKEN = "ODM0NDU3MDY2NzQ3NDYxNjMz.YIBKtA.tBJLp9I4zV79txwPWxyCQ2OEJxs"

client = commands.Bot(command_prefix='mb!')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="mb! help"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    s = message.content.lower().split()

    if s[0] == 'mb!':
        if s[1] == 'getmemeuser':
            q = f'https://flaskprojstud.herokuapp.com/export/{s[2]}/{s[3]}'
            request = requests.get(q)
            if request:
                answ = 'https://flaskprojstud.herokuapp.com/static/' + requests.get(q).json()
                await message.channel.send(answ)
            else:
                await message.chanel.send('Error in image getting')
        elif s[1] == 'getmemepublic':
            await message.channel.send('WIP')
        elif s[1] == 'help':
            await message.channel.send('getmemeuser <username> <key> to get your meme')
            await message.channel.send('getmemepublic <key> to get a public meme')

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
