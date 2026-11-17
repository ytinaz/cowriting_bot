import discord
import os
import re
import random
from dotenv import load_dotenv
from discord.ext import commands
from docx import Document
from datetime import datetime
from pathlib import Path

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
    await ctx.send(f'Start of chapter acknowledged. \n*Please note this command will not work while the bot is offline but functionality is still maintained.*') 
    

@client.command()
async def helpme(ctx):
    await ctx.send(f'To use me, please do the following: \nMark your chapter beginnings with \'!start\' so that I know where to start and end chapters. \nTo export the latest chapter, use !export_last.')


@client.command()
async def export_last(ctx):
    success = False
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
                
                if not message.author.bot and not message_text.startswith('!export_last') and not message_text.startswith('!export_all'): #ignore bot messages + export commands
                    chapter_contents.append(message_text + '\n')

            try:
                os.mkdir("exports")
            except PermissionError:
                 print("Permission denied.")
                 await ctx.send(f'Permission denied - cannot create directory for output')
            except FileNotFoundError:
                print("The parent directory does not exist.")
                await ctx.send(f'Something went wrong :(')
            except FileExistsError:
                print("The directory already exists, ignoring.")
            except OSError as error:
                print("Directory creation failed:", error)
                await ctx.send(f'Could not create directory for output - {error}')

            filename = f'exports/{datetime.now().date()}_{datetime.now().time()}_{ctx.channel}.txt'

            try:
                f = open(filename, "w")
                f.writelines(chapter_contents[::-1])
                f.close()
            except PermissionError:
                 print("Permission denied.")
                 await ctx.send(f'Permission denied - cannot create/write/close file, please manually check {os.getcwd()}/{filename}.')
            except FileNotFoundError:
                print("Can't find the file.")
            except OSError as error:
                print("File creation failed:", error)
                await ctx.send(f'File creation failed - {error}')
            except FileExistsError:
                print("The specified file already exists.")

            await ctx.send(f'Exported to {os.getcwd()}/{filename}. Please double check everything is correct.')
            success = True
            break
    if not success:
        await ctx.send(f'Failed to find most recent !start in channel. Please ensure your chapters are marked correctly.')

#TODO: export ALL using !start as breakpoints/delineate
@client.command()
async def export_all(ctx):
    chapters = []
    chapter_contents = []

    #begin parsing all messages in history from most recent
    async for message in ctx.channel.history():
        message_text = message.content

        #if the message is marked as the start of a chapter, the previous chapter is finished parsing.
        if message_text.startswith('!start'): 
            #remove !start + whitespace and add to chapter_contents
            start_removed = message_text.replace("!start", "")
            start_removed = start_removed.lstrip()
            chapter_contents.append(start_removed + '\n')

            #add full chapter contents into chapters
            chapters.append(chapter_contents)
            
            #empty chapter_contents
            chapter_contents = []
        elif not message.author.bot: #otherwise we want to continue reading, ignoring bot messages.
            if not message_text.startswith('!export_last') and not message_text.startswith('!export_all'): #Make sure to ignore export commands
                chapter_contents.append(message_text + '\n') 
     
    #directory_name = "exports/" + {ctx.channel.name} + "_chapters"
    
    try:
        os.mkdir("exports")
    except PermissionError:
        print("Permission denied.")
        await ctx.send(f'Permission denied - cannot create directory for output')
    except FileNotFoundError:
        print("The parent directory does not exist.")
        await ctx.send(f'Something went wrong :(')
    except FileExistsError:
        print("The directory already exists, ignoring.")
    except OSError as error:
        print("Directory creation failed:", error)
        await ctx.send(f'Could not create directory for output - {error}')

    try:
        os.mkdir(f'exports/{ctx.channel}_chapters')
    except PermissionError:
        print("Permission denied.")
        await ctx.send(f'Permission denied - cannot create directory for output')
    except FileNotFoundError:
        print("The parent directory does not exist.")
        await ctx.send(f'Something went wrong :(')
    except FileExistsError:
        print("The directory already exists, ignoring.")
    except OSError as error:
        print("Directory creation failed:", error)
        await ctx.send(f'Could not create directory for output - {error}')
        

    for chapter in chapters[::-1]:
        filename = f'exports/{ctx.channel}_chapters/{datetime.now().date()}_{datetime.now().time()}_{ctx.channel}.txt'
        try:
            f = open(filename, "w")
            f.writelines(chapter[::-1])
            f.close()
        except PermissionError:
            print("Permission denied.")
            await ctx.send(f'Permission denied - cannot create/write/close file, please manually check {os.getcwd()}/{filename}.')
        except FileNotFoundError:
            print("Can't find the file.")
        except OSError as error:
            print("File creation failed:", error)
            await ctx.send(f'File creation failed - {error}')
        except FileExistsError:
            print("The specified file already exists.")
    

client.run(token)



