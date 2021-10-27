import discord, os, asyncio, random, keep_alive, pyfiglet
from emojis import *
from replit import db
from os import system, name
from discord.ext import commands
from discord.ext.commands import has_permissions

def get_prefix(client,message):
    prefix = db[f'prefix_{message.guild.id}']
    return prefix

my_secret = os.environ['TOKEN']
client = commands.Bot(command_prefix=get_prefix)
logo_systemfall = pyfiglet.figlet_format('By SystemFall')

@client.event
async def on_ready():
    clear()
    print(logo_systemfall)
    print(f'BOT enabled as {client.user}!') 

@client.event
async def on_guild_join(guild):
    db[f'prefix_{guild.id}'] = '.'

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        prefix = db[f'prefix_{message.guild.id}']
        await message.channel.send(f'Bot prefix is {prefix}, you can type {prefix}help for more info')

    await client.process_commands(message)

@client.event
async def on_raw_reaction_add(payload):

    suggestionch = db[f'suggestionch_{payload.guild_id}']
    approvedch = db[f'approvedch_{payload.guild_id}']
    has_admin = payload.member.top_role.permissions.administrator
    user = payload.member
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if user == client.user:
        return

    elif payload.channel_id == suggestionch and payload.emoji.name == emoji_check and has_admin == True:
        approved = client.get_channel(approvedch)
        embed = message.embeds[0]

        embed.title = 'Suggestion approved'
        embed.set_footer(text='')
        msg = await approved.send(embed=embed)
        await msg.add_reaction(emoji_uncheck)
        await message.delete()

    elif payload.channel_id == suggestionch and payload.emoji.name == emoji_check and has_admin == False:
        await message.remove_reaction(emoji_check, user)

    elif payload.channel_id == suggestionch and payload.emoji.name == emoji_uncheck and has_admin == True:
        await message.delete()

    elif payload.channel_id == suggestionch and payload.emoji.name == emoji_uncheck and has_admin == False:
        await message.remove_reaction(emoji_uncheck, user)

    elif payload.channel_id == approvedch and payload.emoji.name == emoji_uncheck and has_admin == True:
        suggestion = client.get_channel(suggestionch)
        embed = message.embeds[0]

        embed.title = 'Suggestion'
        embed.set_footer(text='React with ⬇️ or ⬆️')
        msg = await suggestion.send(embed=embed)
        await msg.add_reaction(emoji_up)
        await msg.add_reaction(emoji_down)
        await msg.add_reaction(emoji_check)
        await msg.add_reaction(emoji_uncheck)
        await message.delete()

    elif payload.channel_id == approvedch and payload.emoji.name == emoji_uncheck and has_admin == False:
        await message.remove_reaction(emoji_uncheck, user)

@client.command()
@has_permissions(administrator=True)
async def setprefix(ctx, arg):
    if ctx.author == client.user:
        return
    db[f'prefix_{ctx.guild.id}'] = arg
    prefix = db[f'prefix_{ctx.guild.id}']
    print(f'prefix set to {prefix}')

@client.command(aliases=['ssc', 'setsgch'])
@has_permissions(administrator=True)
async def setsuggestionchannel(ctx, arg):
    if ctx.author == client.user:
        return

    db[f'suggestionch_{ctx.guild.id}'] = int(arg)

    suggestionch = db[f'suggestionch_{ctx.guild.id}']
    suggestion = client.get_channel(suggestionch)
    perms = suggestion.overwrites_for(ctx.guild.default_role)
    perms.send_messages=False
    perms.add_reactions=False

    await suggestion.set_permissions(ctx.guild.default_role, overwrite=perms)
    await suggestion.purge(limit=1000)
    await suggestion.send(f'This channel has been set as the **suggestion channel** by ``{ctx.author.name}``')
    await ctx.message.delete()

@client.command(aliases=['sac', 'setapch'])
@has_permissions(administrator=True)
async def setapprovedchannel(ctx, arg):
    if ctx.author == client.user:
        return

    db[f'approvedch_{ctx.guild.id}'] = int(arg)

    approvedch = db[f'approvedch_{ctx.guild.id}']
    approved = client.get_channel(approvedch)
    perms = approved.overwrites_for(ctx.guild.default_role)
    perms.send_messages=False
    perms.add_reactions=False

    await approved.set_permissions(ctx.guild.default_role, overwrite=perms)
    await approved.purge(limit=1000)
    await approved.send(f'This channel has been set as the **Approved channel** by ``{ctx.author.name}``')
    await ctx.message.delete()

@client.command(aliases=['refuse', 'delete'])
@has_permissions(administrator=True)
async def deny(ctx, strid, *, reason):
    if ctx.author == client.user:
        return

    id = int(strid)
    message = channel.fetch_message(id)
    user = message.author
    embed = message.embeds[0]


    await user.send('The following suggestion was denied:')
    await user.send(embed=embed)
    await user.send(f'The reason is: ``{reason}``')

@client.command()
async def sugerir(ctx, *, arg):
    if ctx.author == client.user:
        return

    suggestionch = db[f'suggestionch_{ctx.guild.id}']
    suggestion = client.get_channel(suggestionch)
    avatarurl = ctx.author.avatar_url
    embed = discord.Embed(
        title = 'Suggestion',
        description = f'```{arg}```',
        color = discord.Color.blue()
    )

    embed.set_footer(text='React with ⬇️ or ⬆️')
    embed.set_author(name=ctx.author, icon_url=avatarurl)

    message = await suggestion.send(embed=embed)
    await message.add_reaction(emoji_up)
    await message.add_reaction(emoji_down)
    await message.add_reaction(emoji_check)
    await message.add_reaction(emoji_uncheck)
    await ctx.message.delete()

async def chpr():
    await client.wait_until_ready()

    statuses = ['Cyberpunk', 'GTA V', 'Minecraft', 'Tetris', 'Brawhalla']

    while not client.is_closed():
        status = random.choice(statuses)

        await client.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(20)

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
  
keep_alive.keep_alive()
client.loop.create_task(chpr())
client.run(my_secret)
