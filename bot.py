import discord
import os
import re
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

@client.command()
async def start(ctx):
    #print(f"message is {ctx.message.content}")
    message_text = ctx.message.content
    pattern = "^!start \"{1}[^\"]*\"{1}"
    if re.search(pattern, message_text):  #verify command is correct using regex.
        chapter_name = message_text.split("\"")[1]
        #print(f"start of {ctx.channel} and chapter is {chapter_name}")
        await ctx.send(f'Start of **{ctx.channel}: {chapter_name}** acknowledged. \n*Please note this command will not work while the bot is offline but functionality is still maintained.*')
    else:
        await ctx.send(f'Usage: !start "chapter name". Please try again.') 
    
@client.command()
async def finish(ctx):
    async for message in ctx.channel.history():
        print(f"{message.author}: {message.content}")
        message_text = message.content
        if message_text.startswith('!start'): #look for the most recent "!start command"
            #print(f'found the start, exiting loop on {message_text}') 
            pattern = "^!start \"{1}[^\"]*\"{1}" #make sure this one is sane/entered correctly
            if re.search(pattern, message_text):
                chapter_name = message_text.split("\"")[1]
                channel_name = ctx.channel
                await ctx.send(f'found most recent !start that is valid {channel_name} : {chapter_name}')
                #TODO have chapter name and do stuff w it now..
                # pull out to a file
                # parse for formatting
                # upload to gdrive?
            else:
                message_url = discord.MessageReference(message_id=message.id, channel_id=ctx.channel.id).jump_url
                await ctx.send(f'Most recent !start is invalid. Please check the most likely chapter start {message_url} and rectify before running again.')
            break


client.run(token)



