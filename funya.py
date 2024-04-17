import discord
from discord.ext import commands
from discord.utils import get

from hangman import hangman
from randoms import flip_coin, roll_helper
from tictactoe import tictactoe

activity = discord.Activity(type=discord.ActivityType.listening, name="ОСИКЕТТЭЁ, СИКЕТТЭЁ, САНУ СИКУ МИ ФО...")
PREFIX = '/'
intents = discord.Intents.all()
voice = None

funya = commands.Bot(command_prefix=PREFIX, intents=intents, activity=activity)
funya.remove_command("help")


@funya.event
async def on_ready():
    print("Funya connected")


# Споры
@funya.command(pass_context=True)
async def coinflip(ctx):
    await flip_coin(ctx)


@funya.command(pass_context=True)
async def roll(ctx):
    await roll_helper(ctx)


#  Общение
@funya.command(pass_context=True)
async def hello(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')


@funya.command(pass_context=True)
async def bark(ctx):
    await ctx.send('Гав!')


@funya.command(pass_context=True)
async def joinme(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    if channel:
        voice = get(funya.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect(reconnect=True, timeout=None)
    else:
        await ctx.send("You're not in a voice channel!")


@funya.command(pass_context=True)
async def leave(ctx):
    global voice
    voice = get(funya.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect(force=True)
        await ctx.send("I have left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel!")


# Игры
@funya.command(pass_context=True)
async def ttt(ctx, opponent: discord.Member):
    await tictactoe(ctx, opponent)


@funya.command(pass_context=True)
async def hg(ctx):
    await hangman(ctx)


@funya.command(pass_context=True)
async def commands(ctx):
    emb = discord.Embed(title="I can:")

    emb.add_field(name=f'{PREFIX}hello', value='Greet')
    emb.add_field(name=f'{PREFIX}bark', value='Bark')
    emb.add_field(name=f'{PREFIX}coinflip', value='Resolve your disputes')
    emb.add_field(name=f'{PREFIX}roll', value='Resolve your disputes #2')
    emb.add_field(name=f'{PREFIX}joinme', value='Sit with you')
    emb.add_field(name=f'{PREFIX}leave', value='Relax')
    emb.add_field(name=f'{PREFIX}ttt', value='Organize you a Tic-Tac-Toe game')

    await ctx.send(embed=emb)


if __name__ == '__main__':
    funya.run("here is my token")
