from discord_slash.utils.manage_components import create_button, create_actionrow
from discord.player import FFmpegOpusAudio
import discord, os, json
from discord.ext import commands
from dotenv import load_dotenv
from discord_slash import SlashCommand
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext

f = open('site.json',)
data = json.load(f)

intents = discord.Intents.default()
description = """DRadio allows you to listen to the Radio"""
bot = commands.Bot(activity=discord.Activity(type=discord.ActivityType.listening, name="the Radio | r,help", url="https://twitch.tv/0scie"), command_prefix=data['prefix'], status=discord.Status.dnd, description=description, intents=intents)

slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload = True)

load_dotenv()

@bot.command()
async def test(ctx):
    f = open('site.json',)
    data = json.load(f)
    await ctx.send(data['sites'][2])

@bot.command()
async def radio(ctx):
    f = open('site.json',)
    data = json.load(f)

    radiobuttons = [
        create_button(
            style=ButtonStyle.blue,
            label="Controls",
            disabled=True
        ),
        create_button(
            style=ButtonStyle.green,
            label="Join",
            custom_id="radiojoin"
        ),
        create_button(
            style=ButtonStyle.green,
            label="Stop Playing",
            custom_id = "radiostop"
        ),
        create_button(
            style=ButtonStyle.green,
            label="Leave",
            custom_id = "radioleave"
        ),
        create_button(
            style=ButtonStyle.red,
            label="Delete",
            custom_id="radiodelete"
        )
    ]

    stationbuttons1 = [
        create_button(
            style=ButtonStyle.blue,
            label="Stations",
            disabled=True
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][0]['name'],
            custom_id="radioone",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][1]['name'],
            custom_id="radiotwo",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][2]['name'],
            custom_id="radiothree",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][3]['name'],
            custom_id="radiofour",
        ),
    ]

    radiorow = create_actionrow(*radiobuttons)
    stationrow1 = create_actionrow(*stationbuttons1)

    radioembed = discord.Embed(color=discord.Color.purple(), name="Radio", description=f"Hey there {ctx.author.name}, welcome to the radio controls. If you havent already, hop into <#{data['channelid']}>. The buttons below will let you control me.\n\nWant to self host with your own stations? [Click here!](https://github.com/scor57/dradio)\nDonate? [Buy me a Cookie](https://buymeacoffee.com/oscie)")

    await ctx.send(embed=radioembed, components=[radiorow, stationrow1])

@bot.event
async def on_component(ctx: ComponentContext):
    f = open('site.json',)
    data = json.load(f)

    if ctx.custom_id == "radiodelete":
        await ctx.origin_message.delete()

        embed4 = discord.Embed(color=discord.Color.purple(), description="Old message deleted.")
        await ctx.send(embed=embed4, delete_after=5)

    elif ctx.custom_id == "radiojoin":

        guild = bot.get_guild(int(data['guildid']))
        voiceChannel = discord.utils.get(guild.voice_channels, id=int(data['channelid']))
        voice = discord.utils.get(bot.voice_clients, guild=guild)

        if voice == None:
            await voiceChannel.connect()
            embed = discord.Embed(color=discord.Color.purple(), description="Connected to Voice")
            await ctx.send(embed=embed, delete_after=5)

        else:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I am already connected")
            await ctx.send(embed=embed2, delete_after=5)

    elif ctx.custom_id == "radiostop":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()

        embed4 = discord.Embed(color=discord.Color.purple(), description="Stopped Playing")
        await ctx.send(embed=embed4, delete_after=5)

    elif ctx.custom_id == "radioleave":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
        else:
            await voice.disconnect()
            embed2 = discord.Embed(color=discord.Color.purple(), description="Disconnected")
            await ctx.send(embed=embed2, delete_after=5) 



    elif ctx.custom_id == "radioone":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][0]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][0]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radiotwo":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][1]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][1]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radiothree":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][2]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][2]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radiofour":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][3]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][3]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
if __name__ == "__main__":
    f = open('site.json',)
    data = json.load(f)
    bot.run(data['token'], bot=True, reconnect=True)
    
    "ODYyMzgwOTEyNTY4OTU4OTc2.YOXgzw.Lso_uARpVqg7ju3ZrtWIvs7VARE"
