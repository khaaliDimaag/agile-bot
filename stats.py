import os, datetime

import discord
from discord.ext import commands

class khaaliStats(discord.Client):

  def init(self, prefix='?'):
    self.PREFIX = prefix


  async def on_ready(self):
    act = discord.Activity()
    act.type = discord.ActivityType.watching
    act.name = 'who comes here'
    await bot.change_presence(activity=act)
    print('Mein bhi Chowkidaar')

  async def on_message(self, msg):
    pass

  

if __name__=='__main__':
  if not os.environ.get('KHAALI_STATS'): exit('token not found')
  bot = khaaliStats()
  bot.run(os.environ['KHAALI_STATS'])
