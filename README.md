# Voicely 
#### Video Demo:

https://youtu.be/LwsXdm7SUnc

#### Description:
a voice for the voiceless. voicely is a discord bot written in python using the discord.py library. it allows for text-to-speech capabilities in a discord voice call. it monitors a selected text-channel for input, then broadcasts the resultant audio file to the current voice chat. users can choose which text channel they would like the bot to watch. this enables automatic text-to-speech, with no need for a command prefix, in that text channel. additionally, the "(x) said" tts prefix can be toggled on or off guild("server")-wide.

it uses a sqlite3 database file to store per-guild preferences. it features message queueing so that there is no clobbering of previous tts messages being read out loud. 
