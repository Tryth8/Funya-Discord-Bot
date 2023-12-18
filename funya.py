import random
import discord
from discord.ext import commands
from discord.utils import get

activity = discord.Activity(type=discord.ActivityType.listening, name="ОСИКЕТТЭЁ САНУ...")
PREFIX = '/'
intents = discord.Intents.all()

funya = commands.Bot(command_prefix=PREFIX, intents=intents, activity=activity)
funya.remove_command("help")


@funya.event
async def on_ready():
    print("Funya connected")


@funya.command(pass_context=True)
async def hello(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')


@funya.command(pass_context=True)
async def bark(ctx):
    await ctx.send('Гав!')


@funya.command(pass_context=True)
async def tort(ctx):
    await ctx.send('Маликуша - торт!')


@funya.command(pass_context=True)
async def monetka(ctx):
    rand_int = random.randint(0, 10)
    if rand_int < 4:
        await ctx.send(':full_moon: Орёл!')
    elif rand_int < 9:
        await ctx.send(':new_moon: Решка!')
    else:
        await ctx.send(':last_quarter_moon: Монета упала ребром!')


@funya.command(pass_context=True)
async def roll(ctx):
    rand_int = random.randint(0, 101)
    if rand_int < 30:
        await ctx.send(str(rand_int) + "... Маловато шансов...")
    elif rand_int == 47:
        await ctx.send(str(rand_int) + "! И снова Даник...")
    elif rand_int < 55:
        await ctx.send(str(rand_int) + ". Может и выиграешь :thinking:")
    elif rand_int == 69:
        await ctx.send(str(rand_int) + ". Ага, смешно, уау!")
    elif rand_int < 90:
        await ctx.send(str(rand_int) + ". Близок к победе!")
    elif rand_int < 99:
        await ctx.send(str(rand_int) + ". Только попробуй проиграть!")
    elif rand_int == 100:
        await ctx.send(str(rand_int) + ". Гордись! Достижение...")


@funya.command(pass_context=True)
async def joinme(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(funya.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect(reconnect=True, timeout=None)


@funya.command(pass_context=True)
async def relax(ctx):
    await voice.disconnect()


@funya.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title="Я умею:")

    emb.add_field(name='{}hello'.format(PREFIX), value='Приветствовать')
    emb.add_field(name='{}bark'.format(PREFIX), value='Лаять')
    emb.add_field(name='{}tort'.format(PREFIX), value='Хе-хе')
    emb.add_field(name='{}monetka'.format(PREFIX), value='Уметь решать ваши проблемы')
    emb.add_field(name='{}roll'.format(PREFIX), value='Уметь решать ваши проблемы №2')
    emb.add_field(name='{}joinme'.format(PREFIX), value='Сидеть с вами')
    emb.add_field(name='{}relax'.format(PREFIX), value='Чиллить')

    await ctx.send(embed=emb)

funya.run("NzcyNTQwNDk0NzMwNzU2MTE2.GcZIQ1.ZORsasqvL1bbpxzMx-fydlFVbHPuWekEVX1SOE")
