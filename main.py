import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

bot = commands.Bot(command_prefix="*", case_insensitive=True, help_command=None)

extensions = ['misc', 'commands']

count = 0
for ext in extensions:
    bot.load_extension(f"{ext}")
    print(f'{ext} is loaded')
    count += 1


@bot.event
async def on_ready():
    await bot.wait_until_ready()

    await bot.change_presence(activity=discord.Game('*movie'))

    print('--------------------------')
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')
    print('--------------------------')


bot.run(os.environ.get('TOKEN'))
