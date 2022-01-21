import discord
from discord.ext import commands
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

      # removes first element during music playback
      self.music_queue.pop(0)
      # recursive call to check if there is anything else to play
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
      self.is_playing = False

  # check for infinite loops
  async def play_music(self):
    # make sure queue is > 0 before attempting to play
    if len(self.music_queue) > 0:
      self.is_playing = True

      m_url = self.music_queue[0][0]['source']

      # try to connect to voice channel (if not already connected)

      if self.vc == "" or not self.vc.is_connected() or self.vc == None:
        self.vc = await self.music_queue[0][1].connect()
      else:
        await self.vc.move_to(self.music_queue[0][1])

      print(self.music_queue)

      #remove the first element during music playback
      self.music_queue.pop(0)
      # recursive call to check if there is anything else to play
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
      self.is_playing = False


  @commands.command(name="play", help="Plays a selected song from youtube")
  async def p(self, ctx, *args):
    query = " ".join(args)

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
      # must be connected to a voice channel for bot to know where to connect
      await ctx.send("connect to a voice channel first!")
    else:
      song = self.search_yt(query)
      if type(song) == type(True):
        await ctx.send("Song could not be downloaded, please try again!")
      else:
        await ctx.send("Song added to queue!")
        self.music_queue.append([song, voice_channel])

        if self.is_playing == False:
          await self.play_music()

    @commands.command(name="queue", help="Shows current songs in queue")
    async def q(self, ctx):
      retval = ""
      for i in range(0, len(self.music_queue)):
        retval += self.music_queue[i][0]['title'] + "\n"

      print(retval)
      if retval != "":
        await ctx.send(retval)
      else:
        await ctx.send("No music in queue")

    @commands.command(name="skip", help="Skips current song being played")
    async def skip(self, ctx):
      if self.vc != "" and self.vc:
        self.vc.stop()
        # attempt play next in queue if exists
        await self.play_music()

    @commands.command(name="disconnect", help="Disconnect from VC")
    async def dc(self, ctx):
      await self.vc.disconnect()
