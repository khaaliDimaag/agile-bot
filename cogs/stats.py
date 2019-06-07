import os, datetime
import asyncio
import pprint

import discord
from discord.ext import commands

from exceptions import *


class khaaliStats(commands.Cog):
  def __init__(self, bot, db_name='khaaliDiscord', logname='khaaliStats'):
    self.bot = bot
    self.db = self.Database(db_name)
    self.logger = self.Logs(logname)
    self.talk = self.Messages()
    self.cmds = self.Commands(bot)

  @commands.Cog.listener()
  async def on_ready(self):
    print('Mmm lets track some spicy stats')

  @commands.Cog.listener()
  async def on_resumed(self):
    pass

  @commands.Cog.listener()
  async def on_message(self, msg):
    pass

  @commands.Cog.listener()
  async def on_error(self, event, *args):
    pass

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    def is_guild_owner_dm(m): return m.author == guild.owner and type(m) == discord.DMChannel
    YES = ('y','yes','yup','yep'); NO = ('n','no','nup','nope') # TODO: Module for consts?
    dm = guild.owner.dm_channel if guild.owner.dm_channel else guild.owner.create_dm()
    get_stats = False
    if not self.db.exists_in_db(guild.id, 'Guild'):
      new_guild = True
      await dm.send(content=self.talk.first_join(guild.owner), embed=self.talk.channel_id_embed())
      dm.send('Shall I create a stats channel in {0.name}'.format(guild))
      while True:
        try: await msg = self.bot.wait_for('message', check=is_guild_owner_dm, timeout=30.0)
        except asyncio.TimeoutError: await dm.send('Timed out. Shall I?')
        else:
          txt = msg.content.strip().lower()
          if txt in YES:
            perms = {
              guild.default_role: discord.PermissionOverwrite(send_messages=False),
              guild.me: discord.PermissionOverwrite(send_messages=True)
              # Other permissions? add_reactions, 
            }
            await stats = guild.create_channel('stats-chan', overwrites=perms, position=0, topic='Stats for the guild', reason='So khaaliStats can speak in this free country.')
          elif txt in NO:
            get_stats = True
            await dm.send('Alright, send me the stats channel ID', embed=self.talk.channel_id_embed())
            break
          else: await dm.send('Sorry don\'t know what that means. Please try again')
    else:
      new_guild = False
      await dm.send(content=self.talk.rejoin(guild.owner))
      stats = guild.get_channel(self.db.get_stats_channel_id(guild.id)) # Doesn't exist?
      if stats: await dm.send('Is {0.mention} still the stats channel?'.format(stats))
      while True:
        try: await msg = self.bot.wait_for('message', check=is_guild_owner_dm, timeout=30.0)
        except asyncio.TimeoutError: await dm.send('Timed out. Bruh I can\'t do stats if I can\'t speak')
        else:
          txt = msg.content.strip().lower() 
          if txt in YES: 
            break
          elif txt in NO:
            get_stats = True
            await dm.send('Alright, send me the stats channel ID', embed=self.talk.channel_id_embed())
          else: await dm.send('Sorry don\'t know what that means. Please try again')

          else:
      channel = guild.get_channel(txt)
      if channel:
        if self.db.update_stats_channel(guild.id, channel.id):
          await dm.send('Stats channel updated to {0.mention}'.format(channel))
        stats = channel
        break
      else: await dm.send('Some error occurred. Please try again.')
    retries = 0; while get_stats:
      try: await msg = self.bot.wait_for('message', check=is_guild_owner_dm, timeout=30.0)
      except asyncio.TimeoutError: await dm.send('Timed out. Bruh I can\'t do stats if I can\'t speak')
      else:
        txt = msg.content.strip().lower()
        chan = guild.get_channel(txt)
        if not chan: 
          retries+=1
          await dm.send('Channel not found in {0.name}. Please try again'.format(guild))
        else:
          stats = chan
          break
        if retries >= 5:
          await dm.send('It is not that difficult to obtain the channel ID', embed=self.talk.channel_id_embed())
          await dm.send('You can do this!')
    if new_guild: self.db.new_guild(guild)
    else: self.db.update_guild_data('Guild', guild.id, guild)
    self.db.update_guild_data('Member', guild.id, guild.members)
    self.db.update_guild_data('Role', guild.id, guild.roles)
    self.db.update_guild_data('Channel', guild.id, guild.channels)
    self.db.update_guild_data('Webhook', guild.id, guild.webhooks) # Requires `manage_webhooks`
    await stats.send('Here are some spicy stats',embed=self.talk.get_stats_by_guild(guild.id, self.db))

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    pass


  ''' Message ops '''

  @commands.Cog.listener()
  async def on_raw_message_delete(self, payload):
    pass

  @commands.Cog.listener()
  async def on_raw_message_edit(self, payload):
    pass

  @commands.Cog.listener()
  async def on_raw_bulk_message_delete(self, payload):
    pass

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    pass

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    pass

  @commands.Cog.listener()
  async def on_raw_reaction_clear(self, rx):
    pass

  @commands.Cog.listener()
  async def on_private_channel_pins_update(self, channel, last):
    pass

  @commands.Cog.listener()
  async def on_guild_channel_pins_update(self, channel, last):
    pass


  ''' Member ops '''

  @commands.Cog.listener()
  async def on_member_join(self, mem):
    pass

  @commands.Cog.listener()
  async def on_member_remove(self, mem):
    pass

  @commands.Cog.listener()
  async def on_member_ban(self, guild, mem):
    pass

  @commands.Cog.listener()
  async def on_member_unban(self, guild, mem):
    pass


  ''' Role ops '''

  @commands.Cog.listener()
  async def on_guild_role_create(self, role):
    pass

  @commands.Cog.listener()
  async def on_guild_role_delete(self, role):
    pass  

  @commands.Cog.listener()
  async def on_guild_role_update(self, before, after):
    pass


  ''' Channel ops '''

  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
    pass
    
  @commands.Cog.listener()
  async def on_guild_channel_delete(self, channel):
    pass

  @commands.Cog.listener()
  async def on_guild_channel_update(self, before, after):
    pass


  ''' Guild updates '''

  @commands.Cog.listener()
  async def on_guild_update(self, before, after):
    pass

  @commands.Cog.listener()
  async def on_webhooks_update(self, channel):
    pass

  # @commands.Cog.listener()
  # async def on_guild_integrations_update(self, guild):
  #   pass



  # Update from DM instead?
  @commands.command()
  async def update(self, ctx, *args):
    pass


  class Database():
    def __init__(self, db_name):
      self.connection = None
      try: from pymongo import MongoClient
      except ImportError: print('No pyMongo!')
      else: self.connection = MongoClient()[db_name]
      self.collections = {
        'Member': self.connection.members,
        'Channel': self.connection.channels,
        'Role': self.connection.roles,
        'Webhook': self.connection.webhooks,
        'Guild': self.connection.guilds
      }
      self.mongofy = {
        'Member': self.mongofy_member,
        'Channel': self.mongofy_channel,
        'Role': self.mongofy_role,
        'Webhook': self.mongofy_webhook,
        'Guild': self.mongofy_guild
      }

    def exists_in_db(self, id, coll):
      res = None
      if coll in self.collections.keys(): res = self.collections[coll].find({'discord_id': id})
      else: raise InvalidCollection(coll)
      return True if res else False

    def get_stats_channel_id(self, guild_id):
      res = self.collections['Guild'].find({'discord_id': guild_id})
      # Check if ID exists
      return res.stats_chan_id

    def update_stats_channel_id(self, guild_id, channel_id): 
      self.collections['Guild'].find_one_and_update(
        {'discord_id': guild_id}, 
        {'stats_chan_id': channel_id}
      )
    
    def new_guild(self, guild): self.collections['Guild'].insert_one(self.mongofy_guild(guild))
      
    def update_guild_data(coll, guild_id, data):
      if not coll in self.collections.keys(): raise InvalidCollection(coll)
      guild = self.collections['Guild'].find_one({'discord_id':guild_id})
      if coll == 'Guild':
        curr = self.mongofy_guild(data)
        if self.differs(old,current): self.collections['Guild'].find_one_and_update(guild,self.updatify(curr))
        return
      update = guild
      for elem in data:
        obj = None
        if not self.exists_in_db(elem.id,coll): 
          obj = self.collections[coll].insert_one(self.mongofy[coll](elem)).inserted_id
        else:
          res = self.collections[coll].find({'discord_id': elem.id})
          curr = self.mongofy[coll](elem)
          obj = res['_id']
          if self.differs(res,curr): self.collections[coll].find_one_and_update(res, self.updatify(curr))
        update[coll].append(obj)
      self.collections['Guild'].find_one_and_update(guild,update)

    def mongofy_member(self, member):
      return {
        'discord_id': member.id,
        'name': member.name, # Check if same as handle
        'handle': member.discriminator,
        'created': member.created_at,
        'bot': member.bot,
        'nick': member.nick,
        'guilds': {
          member.guild.id: {
            'nick': member.nick,
            'roles': [role.id for role in member.roles],
            'joined': datetime.datetime.now()
          }
        }
      }

    def mongofy_channel(self, channel):
      return {
        'name': channel.name,
        'discord_id': channel.id,
        'created': channel.created_at,
        'guild_id': channel.guild.id,
        'voice': type(channel) == discord.VoiceChannel,
        'category': channel.category.name if channel.category else None
      }

    def mongofy_role(self, role):
      return {
        'name': role.name,
        'discord_id': role.id,
        'value': role.permissions.value,
        'created': role.created_at,
        'guild_id': role.guild.id,
        'managed': role.managed,
        'perms': self.get_perms(role)
      }

    def get_perms(self, role):
      return {
        'general': {
          'create_instant_invite': role.create_instant_invite,
          'kick_members': role.kick_members,
          'ban_members': role.ban_members,
          'administrator': role.administrator,
          'manage_channels': role.manage_channels,
          'manage_guild': role.manage_guild,
          'view_audit_log': role.view_audit_log,
          'stream': role.stream,
          'change_nickname': role.change_nickname,
          'manage_nicknames': role.manage_nicknames,
          'manage_roles': role.manage_roles,
          'manage_webhooks': role.manage_webhooks,
          'manage_emojis': role.manage_emojis
        },
        'text': {
          'read_messages': role.read_messages,
          'send_messages': role.send_messages,
          'send_tts_messages': role.send_tts_messages,
          'manage_messages': role.manage_messages,
          'embed_links': role.embed_links,
          'attach_files': role.attach_files,
          'read_message_history': role.read_message_history,
          'mention_everyone': role.mention_everyone,
          'add_reactions': role.add_reactions,
          'external_emojis': role.external_emojis
        },
        'voice': {
          'connect': role.connect,
          'speak': role.speak,
          'mute_members': role.mute_members,
          'deafen_members': role.deafen_members,
          'move_members': role.move_members,
          'priority_speaker': role.priority_speaker,
          'use_voice_activation': role.use_voice_activation
        }
      }

    def mongofy_webhook(self, webhook):
      return {
        'discord_id': webhook.id,
        'name': webhook.name,
        'token': webhook.token,
        'url': webhook.url,
        'created': webhook.created_at,
        'guild_id': webhook.guild_id
      }

    def mongofy_guild(self, guild, stats=None):
      return {
        'name': guild.name,
        'discord_id': guild.id,
        'owner_id': guild.owner_id,
        'created': guild.created_at,
        'features': guild.features,
        'stats_chan_id': stats,
        'members': [],
        'channels': [],
        'roles': [],
        'webhooks': []
      }

    def updatify(self, doc): return {'$set': doc}

    def differs(self, doc1, doc2):
      for key in doc1.keys():
        if key.startswith('_'): continue
        if doc1.get(key) != doc2.get(key) return True
      return False

  class Messages():
    def __init__(self):
      pass
    
    def welcome_message(self, first):
      if first: return 'You made a wise choice! Let\'s do some stats!'
      else: return 'Thanks for adding me back fam!'

    def channel_id_embed(self):
      em = discord.Embed()
      # em.set_image(url='https://khaalidimaag.io/discord/khaaliStats/channel_id.gif')
      em.set_footer(text=':point_up_2: Send the channel ID fam')  
      em.set_author(name='khaaliStats',url='https://khaalidimaag.io/discord/khaaliStats')
      return em

    def first_join(self, owner):
      pass

    def rejoin(self, owner):
      pass
    
    ''' category default: (all) = int(1111,10) = 15
      b3.b2.b1.b0 = webhooks.roles.channels.members
    '''
    def get_stats_by_guild(self, guild_id, db, category=15):
      em = discord.Embed()
      em.title = 'Spicy stats boiiiiiiii'
      em.description = 'The requested stats are here',
      em.timestamp = datetime.datetime.now(),
      em.color = 0x862D33
      em.set_author(name='khaaliStats', url='https://khaalidimaag.io/bots/khaaliStats')
      if category & 1: # Members
        member_data = ''
        em.add_field(name='Members', value=member_data)
      if category & 2: # Channels
        channel_data = ''
        em.add_field(name='Channels', value=channel_data)
      if category & 4: # Roles
        role_data = ''
        em.add_field(name='Roles', value=roles_data)
      if category & 8: # Webhooks
        webhook_data = ''
        em.add_field(name='Webhooks', value=webhook_data)
      return em

  class Logs():
    def __init__(self, logname):
      import logging
      pass

  class Commands():
    def __init__(self, bot):
      pass

    def parse_commnads(self, txt):
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

def setup(bot): bot.add_cog(khaaliStats(bot))

if __name__=='__main__':
  bot = commands.Bot(command_prefix='~')
  setup(bot)