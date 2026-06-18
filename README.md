Should probably make a proper docker container but im lazy lol

dependencies:
pip install discord.py
pip install python-dotenv

will make this neater. probably.

Currently non functional.
!start "chapter name" - marks the start of the most recent chapter.
!finish - pulls all messages from current message to most recent !start in the current channel. Name is based on channel + "chapter name". Parses text formatting briefly, removes usernames, and uploads to gdocs(?)

