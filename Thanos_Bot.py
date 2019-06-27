import discord
import random
import json


token = '' #insert your token here

def config_read(subject): #function to read from config file
    with open("config.json") as f: #this line opens the json config file with the "with" thing because it handles stuff better
        file = json.loads(f.read()) #reads and loads it as dict
        return file[subject] #returns the value of the subject in the dict (Mode - Kick for example)

class MyClient(discord.Client):
    async def on_ready(self):
        print(self.user.name + ' Online!') #shows a cool message when bot is ready
    async def on_message(self, message):
        if message.content.startswith("!snap"): #this is the main (and only) command
            nonadminmembers = 0 #var that will be used later to count how many non admin members are (because the bot bans/kicks only non admin members)
            if not message.author.permissions_in(message.channel).administrator: #checks if the author of the message has permissions to use the bot
                await message.channel.send('You dont have the right permissions, sorry!') #if he doesn't have perms the bot will say it to him and will just get out of the event thing
                return
            for member in message.guild.members: #loops through all members in server and if the members doesn't have admin it will add 1 to nonadmin var to check how many nonadmin members there are in the server 
                if not member.permissions_in(message.channel).administrator: nonadminmembers +=1 
            chosenmembers = [] #var that will be used later in the list feature thing
            for _ in range(0, nonadminmembers//2): #a loop that loops half of the member count times (to snap half of the non admin members), it floors in case of not even non admin member count.
                rnmember = random.choice(message.guild.members) #first of all it chooses a random member in the server
                while rnmember.permissions_in(message.channel).administrator: #now it loops and finds a new member (incase the random member was an admin) till the  new choosen random member doesn't have admin permissions
                    rnmember = random.choice(message.guild.members)
                if config_read("List"): #now it reads from the config file and checks if the list feature is "turned on"
                    chosenmembers.append(rnmember.name) #if it is it will add the member's name to a list
                if config_read("Mode") == 'Ban': #reads from config file and checks if the mode is ban
                    await rnmember.ban() #if the mode is ban it will ban the random member
                if config_read("Mode") == 'Kick': #reads from config file and checks if the mode is kick
                    await rnmember.kick() #if the mode is kick it will ban the random member
                else: #if the mode isn't kick or ban or the bot is struggling to read the config file or something
                    await message.channel.send('The config file is invalid') #it sends a message to notify the server and exits from the event thing
                    break
            if config_read("Quote"): #after the bans it checks if the quote feature is "turned on"
                await message.channel.send('This server is now perfectly balanced, as all things should be...') #if it is the bot sends the quote to the server
            if config_read("List"): #after the bans it checks if the list feature is "turned on"
                list = "```Victims of " + self.user.name + ':' + '\n' + '\n'.join(chosenmembers) + '```' #this line takes the list that we added stuff to in the for loop and inserts the elements into it to a template i made with lines between the elements
                await message.channel.send(list) #sends takes the string with the list in the template and sends it to the server


client = MyClient()
client.run(token) 
