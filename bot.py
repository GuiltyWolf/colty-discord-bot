import discord
from discord.ext import commands

#imports cogs
from main_cog import main_cog
from music_cog import music_cog

Bot = commands.Bot(command_prefix="gay:")

Bot.add_cog(main_cog(Bot))
Bot.add_cog(music_cog(Bot))

token = ""
with open("token.txt") as file:
  token = file.read()

Bot.run(token)
