# Overview
Guilty Spire is a discord bot that plays music on your hard drive, written in Python 3.7.x using Rapptz's [discord.py](https://github.com/Rapptz/discord.py) API wrapper.

<p align="center">
  <img width="420" height="340" src="guilty_spire.png?raw=true">
</p>

<p align=center><i>God's in his church with his <a href="https://gilescorey.bandcamp.com/track/winters-house">guilty spires</a>.</i></p>

# Current features
- Single-command local music streaming
- Integrated queue for dynamic playback
- Path aliasing for safer, easier queueing

# Features in development
- Pause, resume and stop commands
- Queue editing
- Playlist support

# Requirements
- Python 3.6.x
- discord.py[voice] v1.3.0a
- ffmpeg & ffprobe
- opus

# Installation
1. Create a discord development app and bot account
    - https://github.com/SinisterRectus/Discordia/wiki/Setting-up-a-Discord-application
2. Install discord.py[voice]
    - `pip install -U git+https://github.com/Rapptz/discord.py@master#egg=discord.py[voice]`
3. Download ffmpeg, ffprobe, and opus (place ff executables and opus folder in environment path)
    - ffmpeg & ffprobe: https://ffmpeg.org/download.html
    - opus: http://opus-codec.org/downloads/
4. Create `./config/config.json`:
```json
{
    "token": "token-goes-here"
}
```
# Example usage
**Basic queueing**
```sh
# join voice channel
-harken
-cast path\to\file.mp3
-cast path\to\files
```
*The bot will immediately start playing music and queue everything else*

**Setting a default voice channel**
```sh
# join voice channel
-remember
```
*As long as you're in the newly set default voice channel, you will no longer need to use `-harken` to summon the bot.*

**Creating a path alias**
```sh
-scribe "best album ever" "path\to\files"
-cast best album ever
```
*The bot will recognize the alias and retrieve the path.*

# Contact
- cursethrower#3089
- [twitter](https://twitter.com/cursethrower)
