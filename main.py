import discord
from discord.ext import commands


#imports cogs
from main_cog import main_cog
from music_cog import music_cog

bot = commands.Bot(command_prefix="gay:")

bot.add_cog(main_cog(bot))
bot.add_cog(music_cog(bot))

bot.run(os.getenv("TOKEN"))
