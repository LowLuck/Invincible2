import discord
import requests

TOKEN = "ODM0NDU3MDY2NzQ3NDYxNjMz.YIBKtA.GZ9PiwnyNi5F4CMwl8_GWmadl3o"


class MemeNetworkBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_message(self, message):
        if message.author == self.user:
            return
        s = message.content.lower().split()

        if s[0] == 'mb!':
            if s[1] == 'getmemeuser':
                q = f'https://flaskprojstud.herokuapp.com/export/{s[2]}/{s[3]}'
                request = requests.get(q)
                if request:
                    answ = 'https://flaskprojstud.herokuapp.com/static/' + requests.get(q).json()
                    await message.chanel.send(answ)
                else:
                    await message.chanel.send('Error in image getting')
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


client = MemeNetworkBot()
client.run(TOKEN)
