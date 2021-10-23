import discord, os, asyncio, random, keep_alive
from discord.ext import commands
from discord.ext.commands import has_permissions
from replit import db


my_secret = os.environ['TOKEN']
prefix = db['prefix']
client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
	print(f'Bot enabled as {client.user}! prefix is ( {prefix} )')
	await client.change_presence(status=discord.Status.idle, activity=discord.Game(''))

@client.command()
@has_permissions(administrator=True)
async def setprefix(ctx, arg):
    if ctx.author == client.user:
        return
    db['prefix'] = arg
    prefix = db['prefix']
    print(f'prefix set to {prefix}')

@client.command()
@has_permissions(administrator=True)
async def setsugestionchannel(ctx, arg):
    if ctx.author == client.user:
        return

    db['sugestionch'] = int(arg)

    sugestionch = db['sugestionch']
    sugestion = client.get_channel(sugestionch)
    perms = sugestion.overwrites_for(ctx.guild.default_role)
    perms.send_messages=False
    perms.add_reactions=False

    await sugestion.set_permissions(ctx.guild.default_role, overwrite=perms)
    await sugestion.purge(limit=1000)
    await sugestion.send(f'This channel has been set as the **sugestion channel** by ``{ctx.author.name}``')
    await ctx.message.delete

@client.command()
@has_permissions(administrator=True)
async def setapprovedchannel(ctx, arg):
    if ctx.author == client.user:
        return

    db['approvedch'] = int(arg)

    aprovedch = db['approvedch']
    approved = client.get_channel(approvedch)
    perms = approved.overwrites_for(ctx.guild.default_role)
    perms.send_messages=False
    perms.add_reactions-False

    await approved.set_permissions(ctx.guild.default_role, overwrite=perms)
    await approved.purge(limit=1000)
    await approved.send(f'This channel has been set as the **Approved channel** by ``{ctx.author.name}``')
    await ctx.message.delete

async def chpr():
    await client.wait_until_ready()

    statuses = [f'{prefix}help', 'tetris']

    while not client.is_closed():
        status = random.choice(statuses)

        await client.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(10)

keep_alive.keep_alive()
client.loop.create_task(chpr())
client.run(my_secret)
