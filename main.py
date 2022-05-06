###############
# 05-May-2022 #
###############
#  INTRO BOT  #
#   Jasoos    #
###############

import discord
from funcs import Person,takeIntro
import configparser 
import pdb

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
pdb.set_trace()
commands = config["commands"]

# Variabels
people = []
waitForReaction = False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global waitForReaction
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
            p,reply,response,isEmbed = takeIntro(p1,msg=message)
            people.append(p)
            
        else:
            pass
        await message.reply(reply)
    else:
        # People who are in mid-way process.
        for i in people:
            if i.id == message.author.id:
                if waitForReaction==False:
                    people[people.index(i)], reply, response, isEmbed = takeIntro(i,msg=message)
                    # If response is required.
                    if response==True:
                        if isEmbed == False:
                            await message.reply(reply)
                        else:
                            await message.reply(embed=reply)
                    elif response == "Reaction":
                        waitForReaction = True
                    else:
                        embed = i.returnEmbed()
                        await message.channel.send(embed=embed)
                return
        # If someone messages in between when someone is mid-way.
        await message.reply(f"You can start your own intro process by typing {commands['start']}.")

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
                await reaction.message.reply(reply)
            elif response == "Reaction":
                waitForReaction = True

client.run(config['credentials']['token'])