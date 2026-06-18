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
            pattern = "^!start \"{1}[^\"]*\"{1}" #make sure this one is sane/entered correctly
            if re.search(pattern, message_text):
                chapter_name = message_text.split("\"")[1] #get chapter name and channel name
                channel_name = ctx.channel
                await ctx.send(f'found most recent !start that is valid **{channel_name} : {chapter_name}**. Beginning export...')
                f = open("temporaryA.txt", "w") 
                async for message in ctx.channel.history(): #write all messages until the start message
                    message_text = message.content
                    if re.search(pattern, message_text):
                        #TODO: EXTRACT EXTRA TEXT THAT MIGHT BE AFTER START
                        print(f'{message_text.splitlines()}')
                        if len(message_text.splitlines()) > 2:
                            fields = message_text.splitlines()
                            text_after = fields[2] #this doesnt work for anything above one new line, figure out how we can make this work to pick up stuff
                            #TODO strip newlines

                            print(f'{text_after}')
                        break
                    f.write(f'{message_text}\n')
                #TODO add extra crap at the front if it exists
                f2 = open("temporaryB.txt", "w")
                f.close()
                f = open("temporaryA.txt", "r") #write the messages in correct order in a new file, removing the bot commands.
                lines = f.readlines()
                #print(f'{lines[-2]}')
                if lines[-2].startswith('Start of'): #if the bot was online when the chapter started, remove the acknowledgement lines
                    sliced_lines = lines[2:-2] 
                else:
                    sliced_lines = lines[2:]              
                f2.writelines(sliced_lines[::-1])
                

                await ctx.send(f'exported to file - please double check')

                # pull out to a file (done)
                # parse for formatting (later priority) (TODO)
                # upload to gdrive? (TODO)
            else:
                message_url = discord.MessageReference(message_id=message.id, channel_id=ctx.channel.id).jump_url
                await ctx.send(f'Most recent !start is invalid. Please check the most likely chapter start {message_url} and rectify before running again.')
            break




client.run(token)



