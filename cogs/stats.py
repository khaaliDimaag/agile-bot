import os, datetime
import asyncio
import pprint

import discord
from discord.ext import commands

from .exceptions import *


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
    def is_guild_owner_dm(m): return m.author == guild.owner and type(m.channel) == discord.DMChannel
    YES = ('y','yes','yup','yep'); NO = ('n','no','nup','nope') # TODO: Module for consts?
    dm = guild.owner.dm_channel if guild.owner.dm_channel else await guild.owner.create_dm()
    create_stats = True
    timeouts = 0
    if not self.db.exists_in_db(guild.id, 'Guild'):
      await dm.send(content=self.talk.first_join(guild.owner))
      self.db.new_guild(guild)
      await dm.send('Shall I create a stats channel in {0.name}'.format(guild))
      while True:
        try: msg = await self.bot.wait_for('message', check=is_guild_owner_dm, timeout=60.0)
        except asyncio.TimeoutError: timeouts+=1; await dm.send('Timed out. Shall I create a stats channel!?')
        else:
          txt = msg.content.strip().lower()
          if txt in YES: 
            stats = self.create_stats_channel(guild)
            break
          elif txt in NO:
            create_stats = False
            await dm.send('Alright, send me the stats channel ID', embed=self.talk.channel_id_embed())
            break
          else: await dm.send('Sorry don\'t know what that means. Please try again')
          if timeouts >= 10:
            await dm.send('Sorry but I\'m leaving {0.name} as I do not have a stats channel after 10 minutes. Please add me again')
            await guild.leave()
            return
    else:
      await dm.send(content=self.talk.rejoin(guild.owner))
      self.db.update_guild_data('Guild', guild.id, guild)
      stats = guild.get_channel(self.db.get_stats_channel_id(guild.id))
      if stats: create_stats=False; await dm.send('Is {0.mention} still the stats channel?'.format(stats))
      else: await dm.send('Stats channel not found for {0.name}, shall I create one?'.format(guild))
      while True:
        try: msg = await self.bot.wait_for('message', check=is_guild_owner_dm, timeout=60.0)
        except asyncio.TimeoutError: timeouts+=1; await dm.send('Timed out. Bruh I can\'t do stats if I can\'t speak')
        else:
          txt = msg.content.strip().lower() 
          if txt in YES: 
            if create_stats: stats = self.create_stats_channel(guild)
            break
          elif txt in NO:
            create_stats = False
            await dm.send('Alright, send me the stats channel ID', embed=self.talk.channel_id_embed())
            break
          else: await dm.send('Sorry don\'t know what that means. Please try again')
          if timeouts >= 10:
            await dm.send('Sorry but I\'m leaving {0.name} as I do not have a stats channel after 10 minutes. Please add me again')
            await guild.leave()
            return
    retries = 0
    while not create_stats:
      try: msg = await self.bot.wait_for('message', check=is_guild_owner_dm, timeout=60.0)
      except asyncio.TimeoutError: timeouts+=1; await dm.send('Timed out. Bruh I can\'t do stats if I can\'t speak')
      else:
        txt = msg.content.strip().lower()
        try: txt = int(txt)
        except ValueError: await dm.send('Only channel ID needed; nothing else..'); continue
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
        if timeouts >= 10:
          await dm.send('Sorry but I\'m leaving {0.name} as I do not have a stats channel after 10 minutes. Please add me again')
          await guild.leave()
          return
    self.db.update_guild_data('Member', guild.id, guild.members)
    self.db.update_guild_data('Role', guild.id, guild.roles)
    self.db.update_guild_data('Channel', guild.id, guild.channels)
    # self.db.update_guild_data('Webhook', guild.id, guild.webhooks) # Requires `manage_webhooks`
    await stats.send('Here are some spicy stats',embed=self.talk.get_stats_by_guild(guild.id, self.db))
    await dm.send('Head on to {0.mention} for the current stats'.format(stats))

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


  async def create_stats_channel(self, guild):
    perms = {
      guild.default_role: discord.PermissionOverwrite(send_messages=False),
      guild.me: discord.PermissionOverwrite(send_messages=True)
      # Other permissions? add_reactions, news channel?, 
    }
    channel = await guild.create_channel('stats-chan', overwrites=perms, position=0, topic='Stats for the guild', reason='khaaliStats speaks in this free world')
    return channel

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
        # 'Webhook': self.connection.webhooks,
        'Guild': self.connection.guilds
      }
      self.mongofy = {
        'Member': self.mongofy_member,
        'Channel': self.mongofy_channel,
        'Role': self.mongofy_role,
        # 'Webhook': self.mongofy_webhook,
        'Guild': self.mongofy_guild
      }

    def exists_in_db(self, id, coll):
      if not coll in self.collections.keys(): raise InvalidCollection(coll)
      res = self.collections[coll].find_one({'discord_id': id})
      return True if res else False

    def get_stats_channel_id(self, guild_id):
      res = self.collections['Guild'].find_one({'discord_id': guild_id})
      if not res: raise InvalidGuildID(guild_id)
      return res.get('stats_chan_id', None)

    def update_stats_channel_id(self, guild_id, channel_id): 
      self.collections['Guild'].find_one_and_update(
        {'discord_id': guild_id}, 
        self.updatify({'stats_chan_id': channel_id})
      )
      # Check success?
    
    def new_guild(self, guild): self.collections['Guild'].insert_one(self.mongofy_guild(guild))
      
    def update_guild_data(self, coll, guild_id, data):
      if not coll in self.collections.keys(): raise InvalidCollection(coll)
      guild = self.collections['Guild'].find_one({'discord_id':guild_id})
      if coll == 'Guild':
        curr = self.mongofy_guild(data)
        if self.differs(guild,curr): self.collections['Guild'].find_one_and_update(guild,self.updatify(curr))
        return
      update = guild
      for elem in data:
        obj = None
        if not self.exists_in_db(elem.id,coll): 
          obj = self.collections[coll].insert_one(self.mongofy[coll](elem)).inserted_id
        else:
          res = self.collections[coll].find_one({'discord_id': elem.id})
          curr = self.mongofy[coll](elem)
          obj = res['_id']
          if self.differs(res,curr): self.collections[coll].find_one_and_update(res, self.updatify(curr))
        if update.get(coll): update[coll].append(obj)
        else: update.update({coll:[obj]})
      self.collections['Guild'].find_one_and_update(guild,self.updatify(update))

    def mongofy_member(self, member):
      return {
        'discord_id': member.id,
        'name': member.name, # Check if same as handle
        'handle': member.discriminator,
        'created': member.created_at,
        'bot': member.bot,
        'nick': member.nick,
        'guilds': {
          str(member.guild.id): {
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
        'perms': self.get_perms(role.permissions)
      }

    def get_perms(self, perms):
      return {
        'general': {
          'create_instant_invite': perms.create_instant_invite,
          'kick_members': perms.kick_members,
          'ban_members': perms.ban_members,
          'administrator': perms.administrator,
          'manage_channels': perms.manage_channels,
          'manage_guild': perms.manage_guild,
          'view_audit_log': perms.view_audit_log,
          'stream': perms.stream,
          'change_nickname': perms.change_nickname,
          'manage_nicknames': perms.manage_nicknames,
          'manage_webhooks': perms.manage_webhooks,
          'manage_emojis': perms.manage_emojis
        },
        'text': {
          'read_messages': perms.read_messages,
          'send_messages': perms.send_messages,
          'send_tts_messages': perms.send_tts_messages,
          'manage_messages': perms.manage_messages,
          'embed_links': perms.embed_links,
          'attach_files': perms.attach_files,
          'read_message_history': perms.read_message_history,
          'mention_everyone': perms.mention_everyone,
          'add_reactions': perms.add_reactions,
          'external_emojis': perms.external_emojis
        },
        'voice': {
          'connect': perms.connect,
          'speak': perms.speak,
          'mute_members': perms.mute_members,
          'deafen_members': perms.deafen_members,
          'move_members': perms.move_members,
          'priority_speaker': perms.priority_speaker,
          'use_voice_activation': perms.use_voice_activation
        }
      }

    # def mongofy_webhook(self, webhook):
    #   return {
    #     'discord_id': webhook.id,
    #     'name': webhook.name,
    #     'token': webhook.token,
    #     'url': webhook.url,
    #     'created': webhook.created_at,
    #     'guild_id': webhook.guild_id
    #   }

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

    def updatify(self, doc): return {'$set': doc} # TODO Other update variables

    def differs(self, doc1, doc2):
      for key in doc1.keys():
        if key.startswith('_'): continue
        if doc1.get(key) != doc2.get(key): return True
      return False

  class Messages():
    def __init__(self):
      pass

    def channel_id_embed(self):
      em = discord.Embed()
      # em.set_image(url='https://khaalidimaag.io/discord/khaaliStats/channel_id.gif')
      em.set_footer(text=':point_up_2: Send the channel ID fam')  
      em.set_author(name='khaaliStats',url='https://khaalidimaag.io/discord/khaaliStats')
      return em

    def first_join(self, owner):
      return 'Thanks for adding khaaliStats to your server {0.name}. It is time do something spicy'.format(owner)

    def rejoin(self, owner):
      return 'You kicked me out. You could not live with your own failure. And where did that bring you? Back to me.'
    
    ''' category default: (all) = int(1111,10) = 15
      b3.b2.b1.b0 = webhooks.roles.channels.members
    '''
    def get_stats_by_guild(self, guild_id, db, category=7):
      em = discord.Embed()
      em.title = 'Spicy stats boiiiiiiii'
      em.description = 'The requested stats are here'
      em.timestamp = datetime.datetime.now()
      em.color = 0x862D33
      em.set_author(name='khaaliStats', url='https://khaalidimaag.io/bots/khaaliStats')
      # TODO Shift stats getting to Database
      if category & 1:
        member_data = str(db.collections['Member'].count_documents({'guilds':{str(guild_id):{}}}))
        em.add_field(name='Total Members', value=member_data)
      if category & 2:
        channel_data = str(db.collections['Channel'].count_documents({'guild_id':guild_id}))
        em.add_field(name='Total Channels', value=channel_data)
      if category & 4:
        role_data = str(db.collections['Role'].count_documents({'guild_id':guild_id}))
        em.add_field(name='Total Roles', value=role_data)
      # if category & 8:
      #   webhook_data = str(db.collections['Webhook'].count_documents({'guild_id':guild_id}))
      #   em.add_field(name='Total Webhooks', value=webhook_data)
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