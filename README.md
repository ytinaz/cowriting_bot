# Cowriting Exporter Discord Bot
A simple Discord bot with commands to allow exporting of work which has been cowritten in Discord. 

Made for personal use and thus not optimised.

## Dependencies:
``` 
pip install discord.py
pip install python-dotenv
```

## How to Use:
Use `!start` to mark the beginning of every chapter.

`!export_last` exports the most recently written chapter in the channel, using the last `!start` as its stopping point.

`!export_all` exports all chapters in the channel, breaking chapters apart on occurrences of `!start`.


Files are named by date, time, and channel, and are exported to the current working directory of the bot under a new folder called 'exports'. 

Bulk exports using `!export_all` will make additional folders.