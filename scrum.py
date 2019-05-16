import os, datetime

import discord
from discord.ext import commands

class Scrum_Master(discord.Client):

  def init(self, prefix='?'):
    self.PREFIX = prefix


  async def on_ready(self):
    act = discord.Activity()
    act.type = discord.ActivityType.watching
    act.name = 'your messages'
    await bot.change_presence(activity=act)
    print('Awake and Alive')

  async def on_message(self, msg):
    pass

  

if __name__=='__main__':
  if not os.environ.get('SCRUM_MASTER'): exit('token not found')
  bot = Scrum_Master()
  bot.run(os.environ['SCRUM_MASTER'])
