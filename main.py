###############
# 05-May-2022 #
###############
#  INTRO BOT  #
#   Jasoos    #
###############

import discord
from funcs import Person,takeIntro
import configparser 
from database import apppendMember
import os

"""
Name
Age
Gender
Location ---> State, if Indian else Country
Hobbies

"""
client = discord.Client()

config = configparser.ConfigParser()
config.read("config")
commands = config["commands"]

token = os.environ["token"]
commandsChannel = os.environ["commandsChannel"]
intro = os.environ["intro"]


# Variabels
globalMessages = []

people = []
waitForReaction = False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global waitForReaction
    global globalMessages
    if message.channel.id==int(commandsChannel):
        if message.author == client.user:
            return

        if message.content==commands["start"]:
            # Checking if this person is already in an instance of a running intro.
            alreadyPresent = False
            for i in people:
                if i.id==message.author.id:
                    alreadyPresent = True
                    reply = "You have already given your intro!!!"
            # If the person is new and hasn't started the intro process yet.
            if alreadyPresent==False:
                p1 = Person(message.author)
                p1.pfp = message.author.avatar_url
                p,reply,response,isEmbed = takeIntro(p1,msg=message)
                q = await message.reply(reply)
                p.messages.append(q)
                p.messages.append(message)
                people.append(p)
            else:
                pass
        else:
            # People who are in mid-way process.
            for i in people:
                if i.id == message.author.id:
                    if waitForReaction==False:
                        people[people.index(i)], reply, response, isEmbed = takeIntro(i,msg=message)
                        # If response is required.
                        if response==True:
                            if isEmbed == False:
                                q = await message.reply(reply)
                                i.messages.append(q)
                            else:
                                q = await message.reply(embed=reply)
                                i.messages.append(q)
                        elif response == "Reaction":
                            waitForReaction = True
                        else:
                            if reply!="RESTART":
                                embed = i.returnEmbed()
                                channel = client.get_channel(int(intro))
                                q = await channel.send(embed=embed)
                                try:
                                    apppendMember(i)
                                except:
                                    print("There was some error appending to the database")
                            else:
                                q = await message.channel.send("Please restart then.")
                                globalMessages.append(q)
                            for j in i.messages:
                                try:
                                    await j.delete()
                                except:
                                    pass
                            for k in globalMessages:
                                try:
                                    await k.delete()
                                except:
                                    pass
                            people.pop(people.index(i))
                    return
            # If someone messages in between when someone is mid-way.
            q = await message.reply(f"You can start your own intro process by typing {commands['start']}.")
            globalMessages.append(q)
            globalMessages.append(message)

@client.event
async def on_reaction_add(reaction, user):
    global waitForReaction
    if user == client.user:
        return

    emoji = reaction.emoji
    for i in people:
        if i.id == reaction.message.author.id:    
            people[people.index(i)], reply, response, isEmbed = takeIntro(i,msg=reaction.message)
            # If response is required.
            waitForReaction = False
            if response==True:
                q = await reaction.message.reply(reply)
                i.messages.append(q)
            elif response == "Reaction":
                waitForReaction = True

client.run(token)
