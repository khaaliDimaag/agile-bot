import os, datetime

import discord
from discord.ext import commands

from mongo import guild

class khaaliStats(commands.Cog):
  ''' TODO '''

PREFIX = '!'
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')

@bot.event
async def on_ready():
  act = discord.Activity()
  act.type = discord.ActivityType.streaming
  act.name = 'statistics'
  await bot.change_presence(activity=act)
  print('Mein bhi Chowkidaar')

@bot.event
async def on_message(msg):
  ctx = await bot.get_context(msg)
  print(ctx.__dict__)
  pass

@bot.event
async def on_member_join(mem):
  pass

@bot.event
async def on_member_remove(mem):
  pass

@bot.event
async def on_guild_role_create(role):
  pass

@bot.event
async def on_guild_role_delete(role):
  pass  

@bot.event
async def on_guild_role_update(before, after):
  pass

@bot.event
async def on_member_ban(guild, mem):
  pass

@bot.event
async def on_member_unban(guild, mem):
  pass

@bot.event
async def on_guild_update(before, after):
  pass

@bot.event
async def on_webhooks_update(channel):
  pass

@bot.event
async def on_guild_integrations_update(guild):
  pass

@bot.event
async def on_guild_channel_delete(channel):
  pass

@bot.event
async def on_guild_channel_create(channel):
  pass

@bot.event
async def on_guild_channel_update(before, after):
  pass


@bot.command(pass_context=True)
async def members(ctx, *args):
  pass

@bot.command(pass_context=True)
async def channels(ctx, *args):
  pass

@bot.command(pass_context=True)
async def roles(ctx, *args):
  pass

@bot.command(pass_context=True)
async def all(ctx, *args):
  pass

@bot.command(pass_context=True)
async def help(ctx):
  pass


if __name__=='__main__':
  if not os.environ.get('KHAALI_STATS'): exit('token not found')  
  bot.run(os.environ['KHAALI_STATS'])