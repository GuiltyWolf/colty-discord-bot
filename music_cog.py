import discord
import discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    self.is_playing = False

    # create a 2D array [song, channel]
    self.music_queue = []
    self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_steamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    #store our current channel
    self.vc = ""

  # find the urls on the internet
  def search_yt(self, item):
    with YoutubeDL(self.YDL_OPTIONS) as ydl:
      try:
        info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
      except Exception:
        return False

    return {'source': info['formats'][0]['url'], 'title': info['title']}

  def play_next(self):
    if len(self.music_queue) > 0:
      self.is_playing = True

      # grabs the first url
      m_url = self.music_queue[0][0]['source']

      # removes first element during while being played
      self.music_queue.pop(0)

      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
      self.is_playing = False
