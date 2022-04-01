import discord
from discord.ext import commands
import os
import asyncio
import time
import datetime
import random
import json

client = commands.Bot(command_prefix=".")
bot = client

giveaways = []

Message_IDS = []

class Giveaway(commands.Cog):    
    def __init__(self, client):
        self.client = client
        self.client.wait_until_ready
        self.units = {"s" : 1, "m" : 60, "h" : 3600, "d" : 86400}

    @commands.Cog.listener()
    async def on_ready(self):
      global giveaways

      with open('giveaways.json') as g_f:
        giveaways = json.load(g_f)
      g_f.close()

      self.client.loop.create_task(on_ready_loop(self))
      self.client.loop.create_task(on_ready_loop2(self))

    @commands.command()
    @commands.has_any_role('Staff', 'Moneybags')
    async def giveaway(self, ctx, length : str):
      global giveaways

      with open('giveaways.json', 'r') as g_f:
        giveaways = json.load(g_f)

      botboi = self.client.get_user(928766823401422939)
      emberror=discord.Embed(colour=discord.Colour.red(),description='Giveaway Process Cancelled. Please Speecify A Time Unit\n\n`s/m/h/d`',timestamp=ctx.message.created_at)
      emberror.set_author(name='Error',icon_url='https://cdn.discordapp.com/attachments/707870643789627424/732085341275815997/pngegg.png')
      embcancel=discord.Embed(colour=discord.Colour.red(),description='Giveaway Process Cancelled',timestamp=ctx.message.created_at)
      embcancel.set_author(name=f'{ctx.author} | Giveaway Process',icon_url=ctx.author.avatar_url)
      lengthend = length[-1]
      quantity = int(length[:-1])
      time_unit = lengthend.lower()
      if not time_unit in self.units:
        await ctx.send(embed=emberror,delete_after=5)
        return
      seconds = self.units[time_unit] * quantity
      future = int(time.time()+seconds)
      lengthstr = ""
      if time_unit == "s":
        if quantity == 1:
          lengthstr = "Second"
        else:
          lengthstr = "Seconds"
      if time_unit == "m":
        if quantity == 1:
          lengthstr = "Minute"
        else:
          lengthstr = "Minutes"
      if time_unit == "h":
        if quantity == 1:
          lengthstr = "Hour"
        else:
          lengthstr = "Hours"
      if time_unit == "d":
        if quantity == 1:
          lengthstr = "Day"
        else:
          lengthstr = "Days"     
          
      emb=discord.Embed(colour=0x550A84,timestamp=ctx.message.created_at,description=f'Giveaway process started! Your giveaway is set to last `{quantity} {lengthstr}`\n\nWhat do you want your prize to be?')
      emb.set_author(name=f'{ctx.author} | Giveaway Process',icon_url=ctx.author.avatar_url)
      emb.set_footer(text="Type 'cancel' To Reset Process")
      msg = await ctx.send(embed=emb)

      def check1(m):
        return m.channel == ctx.channel and m.author == ctx.author
      prize=await self.client.wait_for('message',check=check1)
      if prize.content == 'cancel':
        await msg.edit(embed=embcancel, delete_after=3)
        return
      emb2=discord.Embed(colour=0x550A84,timestamp=ctx.message.created_at,description = f'Great! Your Giveaway Prize Will Be `{prize.content}`\n\nHow many winners would you like?\nExample: `2`')
      emb2.set_author(name=f'{ctx.author} | Giveaway Process',icon_url=ctx.author.avatar_url)
      emb2.set_footer(text="Type 'cancel' To Reset Process")
      await msg.edit(embed=emb2)

      def check2(m):
        return m.channel == ctx.channel and m.author == ctx.author
      winnercount = await self.client.wait_for('message',check=check2)
      if winnercount.content == 'cancel':
        await msg.edit(embed=embcancel, delete_after=3)
        return
      emb5=discord.Embed(colour=0x550A84,timestamp=ctx.message.created_at,description=f'Nice! Your Giveaway Will Have `{winnercount.content}` Winner(s)!\n\nPlease mention the channel you want the giveaway hosted in.')
      emb5.set_author(name=f'{ctx.author} | Giveaway Process',icon_url=ctx.author.avatar_url)
      emb5.set_footer(text="Type 'cancel' To Reset Process")
      await msg.edit(embed=emb5)

      def check3(m):
        return m.channel == ctx.channel and m.author == ctx.author
      chan1 = await self.client.wait_for('message',check=check3)
      if chan1.content == 'cancel':
        await msg.edit(embed=embcancel, delete_after=10)
        return

      c = chan1.content[:-1]
      c2 = c[2:]
      
      chanob=self.client.get_channel(int(c2))
      emb3=discord.Embed(colour=0x550A84,timestamp=ctx.message.created_at,description=f'Success! Your Giveaway Has Been Sent To {chanob.mention}')
      emb3.set_author(name=f'{ctx.author} | Giveaway Process',icon_url=ctx.author.avatar_url)
      await msg.edit(embed=emb3, delete_after=5)

      chanlist=[]
      Final=str(f'{quantity}' + " " + lengthstr)
      chanlist.append(Final)
      One_String = " ".join(chanlist)
      value = datetime.datetime.fromtimestamp(seconds)
      days = int(value.strftime('%d'))-1
      time_remaining_str = value.strftime(f'{days} Days, %H Hours, %M Minutes, %S Seconds')

      emb4=discord.Embed(colour=0x550A84,title=':tada: Active Giveaway :tada:')
      emb4.add_field(name='Host:',value=f'{ctx.author}',inline=True)
      emb4.add_field(name='Winners:',value=winnercount.content,inline=True)
      emb4.add_field(name='Date Started:',value=ctx.message.created_at.ctime(),inline=False)
      emb4.add_field(name='Time Remaining:',value=f'{time_remaining_str}',inline=False)
      emb4.add_field(name='Prize:',value=prize.content,inline=False)
      emb4.set_footer(text='React To Enter!',icon_url=ctx.author.avatar_url)

      msgid = await chanob.send(embed=emb4)
      emoji = '🎉'
      await msgid.add_reaction(emoji)


      giveaways['giveaways'] += [{
            "host": int(ctx.author.id),
            "guild": str(ctx.guild),
            "channel": int(chanob.id),
            "end-of-giveaway": int(future),
            "reward": str(prize.content),
            "winner_count": int(winnercount.content),
            "messageid": str(msgid.id),
            "date-started": str(ctx.message.created_at.ctime()),
            "time-remaining": str(One_String),
            "time-remaining-int": int(seconds),
            "entries": []
        }]
      with open('giveaways.json','w') as g_f:
        json.dump(giveaways, g_f, indent=2)

    @giveaway.error
    async def giveaway_error(self, ctx, error):
      await ctx.message.delete()
      emberror=discord.Embed(colour=discord.Colour.red(),description='Missing Required Argument',timestamp=ctx.message.created_at)
      emberror.set_author(name='Error',icon_url='https://cdn.discordapp.com/attachments/707870643789627424/732085341275815997/pngegg.png')
      emberror2=discord.Embed(colour=discord.Colour.red(),description='Insufficient Permissions',timestamp=ctx.message.created_at)
      emberror2.set_author(name='Error',icon_url='https://cdn.discordapp.com/attachments/707870643789627424/732085341275815997/pngegg.png')
      emberror3=discord.Embed(colour=discord.Colour.red(),description=f'An Error Occured: `{error}`\n\nTag Ender With Any Errors',timestamp=ctx.message.created_at)
      emberror3.set_author(name='Error',icon_url='https://cdn.discordapp.com/attachments/707870643789627424/732085341275815997/pngegg.png')
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=emberror, delete_after=10)
      elif isinstance(error, commands.CheckFailure):
        await ctx.send(embed=emberror2, delete_after=10)
      else:
        await ctx.send(embed=emberror3) 

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
      with open('giveaways.json','r') as g_f:
        giveaways = json.load(g_f)

      message_id = payload.message_id

      for giveaway in giveaways['giveaways']:
        if str(message_id) in giveaway['messageid']:
          messageID = payload.message_id
          guild_id = payload.guild_id
          guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)

          member = self.client.get_user(payload.user_id)
          await add_member(giveaway, member, messageID)
    
      with open('giveaways.json','w') as g_f:
        json.dump(giveaways, g_f, indent=2)

  
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
      with open('giveaways.json','r') as g_f:
        giveaways = json.load(g_f)

      message_id = payload.message_id

      for giveaway in giveaways['giveaways']:
        if str(message_id) in giveaway['messageid']:
          messageID = payload.message_id
          guild_id = payload.guild_id
          guild = discord.utils.find(lambda g : g.id == guild_id, self.client.guilds)

          member = self.client.get_user(payload.user_id)
          await remove_member(giveaway, member, messageID)
    
      with open('giveaways.json','w') as g_f:
        json.dump(giveaways, g_f, indent=2)


  
    @commands.command()
    @commands.has_role('Staff')
    async def brokegiveaway(self, ctx):
      await ctx.message.delete()
      chan = self.client.get_channel(928789481476227210)
      msg = await chan.fetch_message(952076742024106014)
      reactions = msg.reactions
      winner = ""
      for reaction in reactions:
        users = await reaction.users().flatten()
        for x in range(4):
          choice = random.choice(users)
          winner += "{}\n".format(choice)
      embed2 = discord.Embed(colour=0x550A84,title=':tada: Giveaway Over! :tada:')
      embed2.add_field(name='Winners:',value=winner,inline=False)
      embed2.add_field(name='Prize:',value='Discord nitro $10 1 month',inline=False)
      embed2.add_field(name='Host:', value='Laval_2000#0551')
      await msg.edit(embed=embed2)

    @commands.command()
    @commands.has_role('Staff')
    async def editgiveaway(self, ctx, arg : str):
      await ctx.message.delete()
      with open('giveaways.json', 'r') as f:
        giveaways = json.load(f)

      def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

      x = await get_giveaway(giveaways['giveaways'], str(arg))
      if x is None:
        pass
      else:

        host = self.client.get_user(x['host'])
        reward = x['reward']
        winner_count = x['winner_count']
        start_date = x['date-started']
        id = x['channel']
        chan = self.client.get_channel(id)
        giveawaymsg = await chan.fetch_message(arg)
        botboi = self.client.get_user(928766823401422939)
        value = datetime.datetime.fromtimestamp(x['time-remaining-int'])
        days = int(value.strftime('%d'))-1
        time_remaining = value.strftime(f'{days} Days, %H Hours, %M Minutes, %S Seconds')

        emb = discord.Embed(colour=0x550A84,timestamp=ctx.message.created_at)
        emb.set_author(name=f'{ctx.author} | Editing Giveaway', icon_url=ctx.author.avatar_url)
        emb.description = f'Current Giveaway Stats:\n\n**1. **Host: `{host}`\n**2.** Reward: `{reward}`\n**3.** Number of Winners: `{winner_count}`\n**4.** Time Remaining: `{time_remaining}`\n\nType the corresponding number to the setting you would like to change. If you would like to end the giveaway now, type `end`. If you would like to cancel this process, type `cancel`.'

        msg = await ctx.send(embed=emb)
        reply = await self.client.wait_for('message', check=check)
        await reply.delete()
        if reply.content == 'cancel':
          emb.description = 'Giveaway edit process cancelled.'
          await msg.edit(embed=emb, delete_after=10)
          pass
        elif reply.content == 'end':
          One_String = ""
          for i in range(x['winner_count']):
            if x['entries'] == []:
              embed2 = discord.Embed(colour=0x550A84,title=':tada: Giveaway Over! :tada:')
              embed2.add_field(name='Winners:',value='None',inline=False)
              embed2.add_field(name='Prize:',value=x['reward'],inline=False)
              embed2.add_field(name='Host:',value=host,inline=False)
              await giveawaymsg.edit(embed=embed2)
              giveaways['giveaways'].remove(x)
              with open('giveaways.json','w') as f:
                json.dump(giveaways, f)
            else:
              winners = x['entries']
              winner = random.choice(winners)
              user = self.client.get_user(int(winner))
              One_String += "{}\n".format(user)
              winners.remove(winner)

          embed = discord.Embed(colour=0x550A84,title=':tada: Giveaway Over! :tada:')
          embed.add_field(name='Winners:',value=One_String,inline=False)
          embed.add_field(name='Prize:',value=x['reward'],inline=False)
          embed.add_field(name='Host:',value=host,inline=False)
      
          await giveawaymsg.edit(embed=embed)
          giveaways['giveaways'].remove(x)
          with open('giveaways.json','w') as f:
            json.dump(giveaways, f)
          emb.description = 'Giveaway ended.'
          await msg.edit(embed=emb, delete_after=10)
        elif reply.content == '1':
          emb.description = 'Please send the ID of the new host. Keep in mind they have to be in this server.'
          await msg.edit(embed=emb)
          reply2 = await self.client.wait_for('message', check=check)
          await reply2.delete()
          newhost = self.client.get_user(int(reply2.content))
          x['host'] = int(reply2.content)
          emb.description = f'`{newhost}` is the new host of this giveaway.'
          emb2=discord.Embed(colour=0x550A84,title=':tada: Active Giveaway :tada:')
          emb2.add_field(name='Host:',value=f'{newhost}',inline=True)
          emb2.add_field(name='Winners:',value=winner_count,inline=True)
          emb2.add_field(name='Date Started:',value=start_date,inline=False)
          emb2.add_field(name='Time Remaining:',value=time_remaining,inline=False)
          emb2.add_field(name='Prize:',value=reward,inline=False)
          emb2.set_footer(text='React To Enter!',icon_url=ctx.author.avatar_url)
          await msg.edit(embed=emb, delete_after=10)
          await giveawaymsg.edit(embed=emb2)
          with open('giveaways.json','w') as f:
            json.dump(giveaways, f)
        elif reply.content == '2':
          emb.description = 'What would you like the new reward to be?'
          await msg.edit(embed=emb)
          reply2 = await self.client.wait_for('message', check=check)
          await reply2.delete()
          x['reward'] = str(reply2.content)
          emb.description = f'`{reply2.content}` is the new reward for this giveaway.'
          emb2=discord.Embed(colour=0x550A84,title=':tada: Active Giveaway :tada:')
          emb2.add_field(name='Host:',value=f'{host}',inline=True)
          emb2.add_field(name='Winners:',value=winner_count,inline=True)
          emb2.add_field(name='Date Started:',value=start_date,inline=False)
          emb2.add_field(name='Time Remaining:',value=time_remaining,inline=False)
          emb2.add_field(name='Prize:',value=reply2.content,inline=False)
          emb2.set_footer(text='React To Enter!',icon_url=ctx.author.avatar_url)
          await msg.edit(embed=emb, delete_after=10)
          await giveawaymsg.edit(embed=emb2)
          with open('giveaways.json','w') as f:
            json.dump(giveaways, f)
        elif reply.content == '3':
          emb.description = 'What is the new number of winners for this giveaway?'
          await msg.edit(embed=emb)
          reply2 = await self.client.wait_for('message', check=check)
          await reply2.delete()
          x['winner_count'] = int(reply2.content)
          emb.description = f'There will now be `{reply2.content}` winners for this giveaway'
          emb2=discord.Embed(colour=0x550A84,title=':tada: Active Giveaway :tada:')
          emb2.add_field(name='Host:',value=f'{host}',inline=True)
          emb2.add_field(name='Winners:',value=reply2.content,inline=True)
          emb2.add_field(name='Date Started:',value=start_date,inline=False)
          emb2.add_field(name='Time Remaining:',value=time_remaining,inline=False)
          emb2.add_field(name='Prize:',value=reward,inline=False)
          emb2.set_footer(text='React To Enter!',icon_url=ctx.author.avatar_url)
          await msg.edit(embed=emb, delete_after=10)
          await giveawaymsg.edit(embed=emb2)
          with open('giveaways.json','w') as f:
            json.dump(giveaways, f)
        elif reply.content == '4':
          emb.description = 'What would you like the new length of the giveaway to be?'
          await msg.edit(embed=emb)
          length = await self.client.wait_for('message', check=check)
          await length.delete()
          lengthend = length.content[-1]
          quantity = int(length.content[:-1])
          time_unit = lengthend.lower()
          if not time_unit in self.units:
            await ctx.send(embed=emberror,delete_after=5)
            return
          seconds = self.units[time_unit] * quantity
          future = int(time.time()+seconds)
          lengthstr = ""
          if time_unit == "s":
            if quantity == 1:
              lengthstr = "Second"
            else:
              lengthstr = "Seconds"
          if time_unit == "m":
            if quantity == 1:
              lengthstr = "Minute"
            else:
              lengthstr = "Minutes"
          if time_unit == "h":
            if quantity == 1:
              lengthstr = "Hour"
            else:
              lengthstr = "Hours"
          if time_unit == "d":
            if quantity == 1:
              lengthstr = "Day"
            else:
              lengthstr = "Days"
          chanlist=[]
          Final=str(f'{quantity}' + " " + lengthstr)
          chanlist.append(Final)
          One_String = " ".join(chanlist)
          x['time-remaining'] = str(One_String)
          x['end-of-giveaway'] = int(future)
          value = datetime.datetime.fromtimestamp(seconds)
          days = int(value.strftime('%d'))-1
          time_remaining_str = value.strftime(f'{days} Days, %H Hours, %M Minutes, %S Seconds')
          emb.description = f'The new giveaway length is now `{One_String}`'
          emb2=discord.Embed(colour=0x550A84,title=':tada: Active Giveaway :tada:')
          emb2.add_field(name='Host:',value=f'{host}',inline=True)
          emb2.add_field(name='Winners:',value=winner_count,inline=True)
          emb2.add_field(name='Date Started:',value=start_date,inline=False)
          emb2.add_field(name='Time Remaining:',value=time_remaining_str,inline=False)
          emb2.add_field(name='Prize:',value=reward,inline=False)
          emb2.set_footer(text='React To Enter!',icon_url=ctx.author.avatar_url)
          await msg.edit(embed=emb, delete_after=10)
          await giveawaymsg.edit(embed=emb2)
          with open('giveaways.json','w') as f:
            json.dump(giveaways, f)
          
          

async def on_ready_loop(self):
  await self.client.wait_until_ready()
  while True:
    await asyncio.sleep(10)
  
    with open('giveaways.json', 'r') as g_f:
      giveaways = json.load(g_f)

    x = await check_giveaway(giveaways['giveaways'], int(time.time()))
    if x is None:
      pass
    else:
      if x['end-of-giveaway'] <= int(time.time()):
        id = x['channel']
        chan = self.client.get_channel(id)
        msgid = x['messageid']
        msg = await chan.fetch_message(msgid)
        host = self.client.get_user(x['host'])
        
        list = []

        One_String = ""
        for i in range(x['winner_count']):
          if x['entries'] == []:
            embed2 = discord.Embed(colour=0x550A84,title=':tada: Giveaway Over! :tada:')
            embed2.add_field(name='Winners:',value='None',inline=False)
            embed2.add_field(name='Prize:',value=x['reward'],inline=False)
            embed2.add_field(name='Host:',value=host,inline=False)
            await msg.edit(embed=embed2)
            giveaways['giveaways'].remove(x)
            with open('giveaways.json','w') as g_f:
              json.dump(giveaways, g_f)
          else:
            winners = x['entries']
            winner = random.choice(winners)
            list.append(winner)
            user = self.client.get_user(int(winner))
            One_String += "{}\n".format(user)
            winners.remove(winner)

        embed = discord.Embed(colour=0x550A84,title=':tada: Giveaway Over! :tada:')
        embed.add_field(name='Winners:',value=One_String,inline=False)
        embed.add_field(name='Prize:',value=x['reward'],inline=False)
        embed.add_field(name='Host:',value=host,inline=False)
      
        await msg.edit(embed=embed)
        giveaways['giveaways'].remove(x)
        with open('giveaways.json','w') as g_f:
          json.dump(giveaways, g_f)
        break
      else:
        pass

async def on_ready_loop2(self):
  await self.client.wait_until_ready()
  while True:
    await asyncio.sleep(30)
  
    with open('giveaways.json', 'r') as g_f:
      giveaways = json.load(g_f)

    for x in giveaways['giveaways']:
      time_remaining_int = x['time-remaining-int']
      id = x['channel']
      chan = self.client.get_channel(id)
      msgid = x['messageid']
      botboi = self.client.get_user(928766823401422939)
      msg = await chan.fetch_message(msgid)
      host = self.client.get_user(x['host'])
      reward = x['reward']
      winner_count = x['winner_count']
      start_date = x['date-started']

      value = datetime.datetime.fromtimestamp(x['time-remaining-int'])
      days = int(value.strftime('%d'))-1
      time_remaining_str = value.strftime(f'{days} Days, %H Hours, %M Minutes, %S Seconds')
      future = x['end-of-giveaway']
      new_time_remaining = int(future-time.time())
      x['time-remaining-int'] = new_time_remaining

      emb2=discord.Embed(colour=0x550A84,title=':tada: Active Giveaway :tada:')
      emb2.add_field(name='Host:',value=f'{host}',inline=True)
      emb2.add_field(name='Winners:',value=winner_count,inline=True)
      emb2.add_field(name='Date Started:',value=start_date,inline=False)
      emb2.add_field(name='Time Remaining:',value=time_remaining_str,inline=False)
      emb2.add_field(name='Prize:',value=reward,inline=False)
      emb2.set_footer(text='React To Enter!',icon_url=ctx.author.avatar_url)
      await msg.edit(embed=emb2)
    with open('giveaways.json','w') as g_f:
      json.dump(giveaways, g_f)
 

async def add_member(giveaway, user, messageID):
  if str(user.id) not in giveaway['entries']:
    if str(user.id) == "928766823401422939":
      return
    else:
      entry_list = giveaway['entries']
      entry_list.append(str(user.id))
  else:
    return

async def remove_member(giveaway, user, messageID):
  if str(user.id) in giveaway['entries']:
    if str(user.id) == "928766823401422939":
      return
    else:
      entry_list = giveaway['entries']
      entry_list.remove(str(user.id))
  else:
    return

async def check_giveaway(list, end):
  for x in list:
    if x['end-of-giveaway'] <= end:
      return x

async def get_giveaway(list, id):
  for x in list:
    if x['messageid'] == id:
      return x

def setup(client):
  t = Giveaway(client)
  client.add_cog(t)