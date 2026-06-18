Should probably make a proper docker container but im lazy lol

dependencies:
pip install discord.py
pip install python-dotenv
 // maybe later pip install python-docx 


 TODO: handle !start "chapter name" and then extra text here - figure out how to consistently get the extra text if present + add to file.
 TODO: handle file conversion/parsing of formatting in MD
 TODO: handle upload, file cleanup (both reverse and forwards)
 TODO: make a dockerfile i guess lol

will make this neater. probably.

Currently non functional.
!start "chapter name" - marks the start of the most recent chapter.
!finish - pulls all messages from current message to most recent !start in the current channel. Name is based on channel + "chapter name". Parses text formatting briefly, removes usernames, and uploads to gdocs(?)

