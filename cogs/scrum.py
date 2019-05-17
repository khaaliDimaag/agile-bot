import os, datetime

import discord
from discord.ext import commands

class Scrum_Master(commands.Cog):
  def __init__(self, bot, prefix='?'):
    self.bot = bot
    self.prefix= prefix

  @commands.Cog.listener()
  async def on_ready(self):
    print('Scrum Master Online!')

  @commands.Cog.listener()
  async def on_message(self, msg):
    pass

def setup(bot): bot.add_cog(Scrum_Master(bot))