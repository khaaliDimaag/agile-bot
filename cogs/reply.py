import os, datetime

import discord
from discord.ext import commands

class khaaliReply(commands.Cog):
  def __init__(self, bot, prefix='>'):
    self.bot = bot
    self.prefix = prefix

  @commands.Cog.listener()
  async def on_ready(self):
    print('Reply Cog active!')

  @commands.Cog.listener()
  async def on_message(self,msg):
    ctx = await self.bot.get_context(msg)
    if not ctx.valid and ctx.prefix == self.prefix: await ctx.invoke(self.reply)
    elif ctx.command: await ctx.invoke(ctx.command)
    else: pass

  @commands.command()
  async def help(self, ctx, *args):
    if len(args)!=0: await ctx.message.channel.send('Usage: `>help` ')
    else:
      em = discord.Embed(
        title='Usage Instructions',
        description='Use this Cog to reply to messages',
        color=0xCDDC96
      )
      em.set_author(name='[bot] khaaliReply')
      em.add_field(name='Commands', value=', '.join(commands), inline=False)
      for command in commands:
        em.add_field(name=command, value=usage[command])
      await ctx.message.channel.send(embed=em)

  @commands.command()
  async def reply(self, ctx, *args):
    reply_to_id = ctx.message.content.split()[0][1:]; em = None
    try: 
      reply_to = await ctx.message.channel.fetch_message(reply_to_id)
      em = self.create_embed(reply_to, ctx.message)
    except discord.NotFound: 
      await ctx.message.channel.send('Message ID: {0} not found in channel'.format(reply_to_id))
      await ctx.invoke(help)
    except discord.Forbidden: 
      await ctx.message.channel.send('I do not have access to the message being referred to!')
    await ctx.message.channel.send(embed=em)

  def create_embed(self, reply_to, reply):
    reply_msg = ' '.join(reply.clean_content.split(' ')[1:])
    embeds = reply_to.embeds
    attached = reply_to.attachments

    em = discord.Embed()
    em.title = ':point_up_2: {0.author.display_name}\'s message is a reply to {1.author.display_name} :point_down:'.format(reply,reply_to)
    em.color = 0x44BFC1
    em.timestamp = reply.created_at

    if attached and reply_msg:
      em.add_field(name='Original Message',value='[Embedded content]({0.jump_url})'.format(reply_to),inline=False)
      for ext in ['.jpg','.jpeg','.png','.gif']:
        if attached[0].url.endswith(ext): em.set_image(url=attached[0].url); break
      else:
        for f in attached: em.add_field(name='Attached file', value='{0.url}'.format(f))
    elif embeds and reply_msg:
      if reply_to.clean_content: em.add_field(name='Original Message',value='[{0.clean_content}]({0.jump_url})'.format(reply_to),inline=False)
      else: em.add_field(name='Original Message',value='[Embedded content]({0.jump_url})'.format(reply_to),inline=False)
    elif reply_msg: em.add_field(name='Original Message',value='[{0.clean_content}]({0.jump_url})'.format(reply_to),inline=False)
    else: pass

    em.add_field(name='Reply',value='[{0}]({1.jump_url})'.format(reply_msg,reply),inline=False)
    em.set_footer(text='Click the links to jump to the messages')
    return em

def setup(bot): bot.add_cog(khaaliReply(bot))