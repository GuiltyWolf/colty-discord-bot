import discord
from discord.ext import commands
import os


#imports cogs
from main_cog import main_cog
from music_cog import music_cog


bot = commands.Bot(command_prefix="gay:")

bot.add_cog(main_cog(bot))
bot.add_cog(music_cog(bot))

token = ""
with open("token.txt") as file:
  token = file.read()

bot.run(token)
