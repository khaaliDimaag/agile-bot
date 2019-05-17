import os, datetime

import discord
from discord.ext import commands

from db import guild

class khaaliStats(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print('Stats online!')

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
  async def all(self, ctx, *args):
    pass

def setup(bot): bot.add_cog(khaaliStats(bot))