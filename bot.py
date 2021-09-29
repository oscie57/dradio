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
bot = commands.Bot(activity=discord.Activity(type=discord.ActivityType.listening, name="to the Radio | r,help", url="https://twitch.tv/0scie"), command_prefix=data['prefix'], status=discord.Status.dnd, description=description, intents=intents)

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
            custom_id="radio0",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][1]['name'],
            custom_id="radio1",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][2]['name'],
            custom_id="radio2",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][3]['name'],
            custom_id="radio3",
        )
    ]

    stationbuttons2 = [
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][4]['name'],
            custom_id="radio4",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][5]['name'],
            custom_id="radio5",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][6]['name'],
            custom_id="radio6",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][7]['name'],
            custom_id="radio7",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][8]['name'],
            custom_id="radio8",
        )
    ]

    stationbuttons3 = [
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][9]['name'],
            custom_id="radio9",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][10]['name'],
            custom_id="radio10",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][11]['name'],
            custom_id="radio11",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][12]['name'],
            custom_id="radio12",
        ),
        create_button(
            style=ButtonStyle.grey,
            label=data['sites'][13]['name'],
            custom_id="radio13",
        )
    ]

    radiorow = create_actionrow(*radiobuttons)
    stationrow1 = create_actionrow(*stationbuttons1)
    stationrow2 = create_actionrow(*stationbuttons2)
    stationrow3 = create_actionrow(*stationbuttons3)

    radioembed = discord.Embed(color=discord.Color.purple(), name="Radio", description=f"Hey there {ctx.author.name}, welcome to the radio controls. If you havent already, hop into <#{data['channelid']}>. The buttons below will let you control me.\n\nWant to self host with your own stations? [Click here!](https://github.com/scor57/dradio)\nDonate? [Buy me a Cookie](https://buymeacoffee.com/oscie)")

    await ctx.send(embed=radioembed, components=[radiorow, stationrow1, stationrow2, stationrow3])

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



    elif ctx.custom_id == "radio0":

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

    elif ctx.custom_id == "radio1":

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

    elif ctx.custom_id == "radio2":

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

    elif ctx.custom_id == "radio3":

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

    elif ctx.custom_id == "radio4":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][4]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][4]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)
    
    elif ctx.custom_id == "radio5":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][5]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][5]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radio6":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][6]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][6]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radio7":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][7]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][7]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radio8":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][8]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][8]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radio9":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][9]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][3]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radio10":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][10]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][10]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radio11":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][11]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][11]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radio12":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][12]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][12]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

    elif ctx.custom_id == "radio13":

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            embed2 = discord.Embed(color=discord.Color.purple(), description="I'm not in the Voice Chat yet!")
            await ctx.send(embed=embed2, delete_after=5)
            return
        else:
            voice.stop()

        src = FFmpegOpusAudio(data['sites'][13]['url'])
        voice.play(src, after=lambda e: print('Player error: %s' % e) if e else None)

        embed3 = discord.Embed(color=discord.Color.purple(), description=f"Now playing: `{data['sites'][13]['name']}`")
        await ctx.send(embed=embed3, delete_after=5)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
if __name__ == "__main__":
    f = open('site.json',)
    data = json.load(f)
    bot.run(data['token'], bot=True, reconnect=True)