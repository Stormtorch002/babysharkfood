from discord.ext import commands
from config import *
import asyncpg
import discord


bot = commands.Bot(
    command_prefix='!',
    case_insensitive=True,
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name='baby shark on yt'
    )
)

COGS = (
    'jishaku',
    'cogs.counting',
    'cogs.servercounts'
)
QUERIES = (
    '''CREATE TABLE IF NOT EXISTS counting (
        "id" SERIAL PRIMARY KEY,
        "next" INTEGER,
        "author_id" BIGINT
    )''',
)


async def on_ready():
    bot.db = await asyncpg.create_pool(**POSTGRES)
    [await bot.db.execute(query) for query in QUERIES]
    await bot.wait_until_ready()
    [bot.load_extension(cog) for cog in COGS]
    print('Ready')


bot.loop.create_task(on_ready())
bot.run(TOKEN)
