import discord
from discord.ext import commands

Bot = commands.Bot(command_prefix='gay:')

@Bot.command()
async def echo(ctx, *args):
  m_args = " ".join(args)
  await ctx.send(m_args)

token = ""
with open("token.txt") as file:
  token = file.read()

Bot.run(token)
