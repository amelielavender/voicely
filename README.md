# Voicely 
#### Video Demo:

https://youtu.be/LwsXdm7SUnc

#### Description:
a voice for the voiceless. voicely is a discord bot written in python using the discord.py library. it allows for text-to-speech capabilities in a discord voice call. it monitors a selected text-channel for input, then broadcasts the resultant audio file to the current voice chat. users can choose which text channel they would like the bot to watch. this enables automatic text-to-speech, with no need for a command prefix, in that text channel. additionally, the "(x) said" tts prefix can be toggled on or off guild("server")-wide.

it uses a sqlite3 database file to store per-guild preferences. it features message queueing so that there is no clobbering of previous tts messages being read out loud. 

different related functions are seperated out into a cogs folder for ease of reading and organization purposes. 
- guild_prefs: holds guild-related preferences
- tts: holds all of the main text-to-speech functions and features
- dbg: various debugging functions

each cog is easily called and/or removed as needed thanks to the discord.py library's features. cogs allow for a more modular approach to a discord bot. 

main.py starts the bot application and features some hidden maintainence commands, such as unloading, loading, and reloading cogs. it also accesses the user's .env file, if available. 
