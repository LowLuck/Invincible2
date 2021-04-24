import discord
import requests

TOKEN = "ODM0NDU3MDY2NzQ3NDYxNjMz.YIBKtA.Or_ntTqILtFeylTL4uKvI-EbLr4"


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
        if 'mb!' in message.content.lower()[0:3]:
            if ' getmeme' in message.content.lower()[3:11]:
                q = 'https://flaskprojstud.herokuapp.com/export/' + message.content[12:]
                request = requests.get(q)
                if request:
                    answ = 'https://flaskprojstud.herokuapp.com/static/' + requests.get(q).json()
                else:
                    answ = 'Error in image getting'
            else:
                answ = 'repy'
        try:
            await message.channel.send(answ)
        except Exception:
            pass


client = MemeNetworkBot()
client.run(TOKEN)
