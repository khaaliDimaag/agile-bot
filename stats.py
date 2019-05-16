import os, datetime
import discord
from discord.ext import commands
# Move inside v

class khaaliStats(discord.Client):

  def init(self, prefix='!'):
    self.PREFIX = prefix

  ''' Events '''

  async def on_ready(self):
    act = discord.Activity()
    act.type = discord.ActivityType.watching
    act.name = 'who comes here'
    await bot.change_presence(activity=act)
    print('Mein bhi Chowkidaar')

  async def on_message(self, msg):
    pass

  async def on_member_join(self, mem):
    pass

  async def on_member_remove(self, mem):
    pass

  async def on_guild_role_create(self, role):
    pass

  async def on_guild_role_delete(self, role):
    pass  

  async def on_guild_role_update(self, before, after):
    pass

  async def on_member_ban(self, guild, mem):
    pass

  async def on_member_unban(self, guild, mem):
    pass

  async def on_guild_update(self, before, after):
    pass

  async def on_webhooks_update(self, channel):
    pass
  
  async def on_guild_integrations_update(self, guild):
    pass

  async def on_guild_channel_delete(self, channel):
    pass
  
  async def on_guild_channel_create(self, channel):
    pass

  async def on_guild_channel_update(self, before, after):
    pass

  ''' Commands '''

  async def members(ctx):
    pass
  
  async def channels(ctx):
    pass
  
  async def roles(ctx):
    pass
  
  async def all(ctx):
    pass

  async def help(ctx):
    pass
  


if __name__=='__main__':
  if not os.environ.get('KHAALI_STATS'): exit('token not found')
  bot = khaaliStats()
  bot.run(os.environ['KHAALI_STATS'])