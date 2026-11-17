import discord
import os
import re
import random
from dotenv import load_dotenv
from discord.ext import commands
from docx import Document

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
        message_text = message.content
        if message_text.startswith('!start'): #look for the most recent "!start command"
            start_message_url = discord.MessageReference(message_id=message.id, channel_id=ctx.channel.id).jump_url
            start_message_id = message.id
            await ctx.send(f'Found most recent !start at {start_message_url} with id {start_message_id}. Beginning export...')

            chapter_contents = []
            async for message in ctx.channel.history(): 
                message_text = message.content
                if message.id == start_message_id:
                    start_removed = message_text.replace("!start", "")
                    start_removed = start_removed.lstrip()
                    chapter_contents.append(start_removed + '\n')
                    break
                
                if not message.author.bot: #ignore bot messages.
                    chapter_contents.append(message_text + '\n')
            
            #TODO: handle no !start found.
            #TODO: neaten error handling/messages
                
            chapter_contents = chapter_contents[1::] #remove !finish message

            print(chapter_contents)
            f = open("temporaryA.txt", "w")
            f.writelines(chapter_contents[::-1])

            await ctx.send(f'Exported to file - please double check')

            break


        #TODO: export ALL using !start as breakpoints/delineate



client.run(token)



