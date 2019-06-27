import discord
import random
import json


token = ''
def config_read(subject):
    with open("config.json") as f:
        file = json.loads(f.read())
        return file[subject]

class MyClient(discord.Client):
    async def on_ready(self):
        print(self.user.name + ' Online!')
    async def on_message(self, message):
        if message.content.startswith("!snap"):
            nonadminmembers = 0
            if not message.author.permissions_in(message.channel).administrator:
                await message.channel.send('You dont have the right permissions, sorry!')
                return
            for member in message.guild.members:
                if not member.permissions_in(message.channel).administrator: nonadminmembers +=1
            chosenmembers = []
            for _ in range(0, nonadminmembers//2):
                rnmember = random.choice(message.guild.members)
                while rnmember.permissions_in(message.channel).administrator:
                    rnmember = random.choice(message.guild.members)
                if config_read("List"):
                    chosenmembers.append(rnmember.name)
                if config_read("Mode") == 'Ban':
                    await rnmember.ban()
                if config_read("Mode") == 'Kick':
                    await rnmember.kick()
                else:
                    await message.channel.send('The config file is invalid')
                    break
            if config_read("Quote"):
                await message.channel.send('This server is now perfectly balanced, as all things should be...')
            if config_read("List"):
                list = "```Victims of Thanos_Bot:" + '\n' + '\n'.join(chosenmembers) + '```'
                await message.channel.send(list)


client = MyClient()
client.run(token)