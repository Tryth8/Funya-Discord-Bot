import random


async def flip_coin(ctx):
    rand_int = random.randint(0, 10)
    if rand_int < 4:
        await ctx.send(':full_moon: Орёл!')
    elif rand_int < 9:
        await ctx.send(':new_moon: Решка!')
    else:
        await ctx.send(':last_quarter_moon: Монета упала ребром!')


async def roll_helper(ctx):
    rand_int = random.randint(0, 101)
    if rand_int < 30:
        await ctx.send(str(rand_int) + "... Too low...")
    elif rand_int == 47:
        await ctx.send(str(rand_int) + "! And once again, Danik...")
    elif rand_int < 55:
        await ctx.send(str(rand_int) + ". Maybe you'll win :thinking:")
    elif rand_int == 69:
        await ctx.send(str(rand_int) + ". 69, yeah, hilarious, wow!")
    elif rand_int < 90:
        await ctx.send(str(rand_int) + ". Likely to win!")
    elif rand_int < 99:
        await ctx.send(str(rand_int) + ". Just try to lose!")
    elif rand_int == 100:
        await ctx.send(str(rand_int) + ". Be proud! Achievement...")
