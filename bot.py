import os
import logging # TODO

import discord
from discord.ext import commands

from reply import setup as reply_cog
# from stats import setup as stats_cog
# from scrum import setup as scrum_cog

def get_prefix(bot, msg):
  prefixes = ['?!', 'bot ', '>']

  return commands.when_mentioned_or(*prefixes)(bot,msg)

bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
  act = discord.Activity()
  act.type = discord.ActivityType.watching
  act.name = 'your messages'
  await bot.change_presence(activity=act)
  print('What is life?')

async def on_message(msg):
  ctx = await bot.get_context(msg)
  if ctx.command: ctx.invoke(ctx.command)
  else: pass

if __name__=='__main__':
  if not os.environ.get('KHAALI_BOT'): exit('token not found')  
  reply_cog(bot)
  # stats_cog(bot)
  # scrum_cog(bot)
  bot.run(os.environ['KHAALI_BOT'])