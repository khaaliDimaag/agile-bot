import os, datetime
import asyncio

import discord
from discord.ext import commands
from pymongo import MongoClient # Use RDBMS?

import logging
# logging.basicConfig(format='[%(asctime)s] - (%(name)s) - %(levelname)s: %(message)s')

class khaaliStats(commands.Cog):
  def __init__(self, bot, db_name='khaaliDiscord', logname='khaaliStats'):
    self.bot = bot
    self.db = MongoClient()[db_name]
    self.logger = logging.getLogger(logname)
    # TODO logger setup

  @commands.Cog.listener()
  async def on_ready(self):
    for guild in self.bot.guilds: 
      self.setup_guild(guild)
    print('Lets track some spicy stats')

  @commands.Cog.listener()
  async def on_message(self, msg):
    pass

  @commands.Cog.listener()
  async def on_member_join(self, mem):
    pass

  @commands.Cog.listener()
  async def on_member_remove(self, mem):
    pass

  @commands.Cog.listener()
  async def on_guild_role_create(self, role):
    pass

  @commands.Cog.listener()
  async def on_guild_role_delete(self, role):
    pass  

  @commands.Cog.listener()
  async def on_guild_role_update(self, before, after):
    pass

  @commands.Cog.listener()
  async def on_member_ban(self, guild, mem):
    pass

  @commands.Cog.listener()
  async def on_member_unban(self, guild, mem):
    pass

  @commands.Cog.listener()
  async def on_guild_update(self, before, after):
    pass

  @commands.Cog.listener()
  async def on_webhooks_update(self, channel):
    pass

  @commands.Cog.listener()
  async def on_guild_integrations_update(self, guild):
    pass

  @commands.Cog.listener()
  async def on_guild_channel_delete(self, channel):
    pass

  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
    pass

  @commands.Cog.listener()
  async def on_guild_channel_update(self, before, after):
    pass


  @commands.command()
  async def members(self, ctx, *args):
    pass

  @commands.command()
  async def channels(self, ctx, *args):
    pass

  @commands.command()
  async def roles(self, ctx, *args):
    pass

  @commands.command()
  async def projects(self, ctx, *args):
    pass

  @commands.command()
  async def all(self, ctx, *args):
    pass

  # Update from DM instead?
  @commands.command()
  async def update(self, ctx, *args):
    pass


  def setup_guild(self, guild):
    query = self.db.guilds.find({'id':guild.id})
    current = {
      'name': guild.name,
      'id': guild.id,
      'owner_id': guild.owner_id
    }
    if query:
      if guild.get_channel(query.stats_chan_id): current.stats_chan_id = query.stats_chan_id
      else: current.stats_chan_id = self.get_stats_chan(guild,first=False)
      if current != query: self.db.guilds.update_one(query,current)
    else:
      current.stats_chan_id = self.get_stats_chan(guild)
      self.db.guilds.insert_one(current)
    self.update_guild_in_db(guild)
    self.send_stats(guild.get_channel(current.stats_chan_id))
    
  def update_guild_in_db(self,guild):
    for member in guild.members:
      # Add to db
      pass
    for role in guild.roles:
      # Add to db
      pass
    for channel in guild.channels:
      # Add to db
      pass
    pass

  def get_stats_chan(self, guild, first=True):
    owner = guild.get_member(guild.owner_id)
    dm = await owner.create_dm() if not owner.dm_channel else owner.dm_channel
    def check(m): return m.channel.id == dm.id and m.author == owner_id
    await dm.send(content=self.welcome_message(first), embed=self.channel_id_embed())
    while True:
      try: msg = await self.bot.wait_for('message', check=check, timeout=60.0)
      except asyncio.TimeoutError: await dm.send('Dont leave me hanging buddy!')
      else: 
        stats = guild.get_channel(msg.content)
        if not stats: 
          await dm.send('Channel not found in {0.name}. Please send the ID again.'.format(guild))
          continue
        if type(stats) != discord.TextChannel:
          await dm.send('Channel is not a Text Channel. How am I supposed to send stats?')
          continue
        await dm.send('Head on over to {0.mention} for the current stats of {1.name}'.format(stats,guild))
        return stats.id


  def welcome_message(self, first):
    if first: return 'You made a wise choice! Let\'s do some stats!'
    else: return 'Thanks for adding me back fam!'

  def channel_id_embed(self):
    em = discord.Embed()
    # em.set_image(url='https://khaalidimaag.io/discord/khaaliStats/channel_id.gif') # NOTE: Link not active
    em.set_footer(text=':point_up_2: Send the channel ID fam')  
    em.set_author(name='khaaliStats',url='https://khaalidimaag.io/discord/khaaliStats')
    return em


  ''' category: int(b3.b2.b1.b0,10)
    b0: members
    b1: channels
    b2: roles
    b3: projects
    default: (all) = int(1111,10) = 15
  '''
  def send_stats(channel, category=15):
    em = discord.Embed(
      title='Current stats of {0.name}'.format(channel.guild),
      timestamp=datetime.datetime.now(),
      color=0xFFFFFF
    )
    # TODO Add data lol
    em.set_author(name='khaaliStats',url='https://khaalidimaag.io/discord/khaaliStats')
    await channel.send(embed=em)


def setup(bot): bot.add_cog(khaaliStats(bot))