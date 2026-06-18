import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

default_intents = discord.Intents.default()
default_intents.message_content = True
client = commands.Bot(command_prefix='!', intents=default_intents)

token = os.getenv('TOKEN')

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

#@client.command()
#async def start(ctx):
    #TODO input verification
    #TODO add acknowledgement
    #await ctx.send('Start of <channel name>: chapter <> noted.')

    
@client.command()
async def finish(ctx):
    async for message in ctx.channel.history():
        print(f"{message.author}: {message.content}")
        if message.content.startswith('!start'): #look for the most recent "!start command"
            print(f'found the start, exiting loop on {message.content}')
            #extract the name of the chapter and the channel name. 
            break
        #from here go backwards until we find the start message
        #make a file given a certain name?
    #print(f'identified command.')
    #await ctx.send('pong')
    await ctx.send('command identified, please see console log.')


client.run(token)



