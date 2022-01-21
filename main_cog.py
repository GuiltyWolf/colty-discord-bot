import discord
from discord.ext import commands

class main_cog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.help_message = """hehe"""
    self.text_channel_list = []

  @commands.Cog.listener()
  async def on_ready(self):
    for guild in self.bot.guilds:
      for channel in guild.text_channels:
        self.text_channel_list.append(channel)

    await self.send_to_all(self.help_message)

  #@commands.command(name="help", help="Displays all the available commands")
  #async def help(self, ctx):
    #await ctx.send(self.help_message)

  #async def send_to_all(self, msg):
    #for text_channel in self.text_channel_list:
      #await text_channel.send(msg)

  @commands.command(name="clear", help="Clear specified amount of messages")
  async def clear(self, ctx, arg):
    amount = 5
    try:
      amount = int(arg)
    except Exception: pass

    await ctx.channel.purge(limit=amount)
