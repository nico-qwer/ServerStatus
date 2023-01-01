# Imports
import discord
import logsmaker
from discord.ext import commands
from mcstatus import JavaServer

# Read values from txt files
with open('token.txt', 'r') as token_file:
    token = token_file.readline()
with open('serverIP.txt', 'r') as IP_file:
    server_ip = IP_file.readline()

# Setup bot
intents = discord.Intents.all()
command_prefix = "$"
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.remove_command("help")

# Setup mcstatus
server = JavaServer.lookup(server_ip)

# Warn nico_qwer that mc server is offline
async def offline_notif(ctx):
    await ctx.send("The server did not answer, it's probably offline. I will be contacting nico_qwer so he can fix this.")

    user = await bot.fetch_user("800394501158862859")
    await user.send("Minecraft server is offline!!")

    logsmaker.error("Server offline.")

# commands
@bot.command()
async def echo(ctx: commands.Context):
    await ctx.send("Hello!")
    logsmaker.info(f"Command used. Author: {ctx.author}. Channel: {ctx.channel}. Command: echo.")

@bot.command()
async def status(ctx: commands.Context):
    try:
        status = server.status()
    except TimeoutError:
        await offline_notif(ctx)
        return

    s = ""
    if status.players.online != 1 :
        s = "s"

    embed = discord.Embed(
        title=f"Current server status:", 
        color=0x7aa660
    )

    embed.add_field(name="Players online:", value=f"{status.players.online} player{s}", inline=False)
    embed.add_field(name="Latency:", value=f"{round(status.latency, 2)} ms", inline=False)
    embed.add_field(name="Version:", value=f"{status.version.name}", inline=False)

    embed.set_footer(text=f"Server IP: {server_ip}")

    await ctx.send(embed=embed)
    logsmaker.info(f"Command used. Author: {ctx.author}. Channel: {ctx.channel}. Command: status.")

@bot.command()
async def ping(ctx: commands.Context):
    try:
        latency = server.ping()
    except TimeoutError:
        await offline_notif(ctx)
        return

    await ctx.send(f"The server replied in {round(latency, 2)} ms")
    logsmaker.info(f"Command used. Author: {ctx.author}. Channel: {ctx.channel}. Command: ping.")

@bot.command()
async def players(ctx: commands.Context):
    try:
        query = server.query()
    except TimeoutError:
        await offline_notif(ctx)
        return

    if query.players.names == []:
        await ctx.send("There are no players online.")
        logsmaker.info(f"Command used. Author: {ctx.author}. Channel: {ctx.channel}. Command: players.")
        return

    player_list = ""
    for name in query.players.names:
        player_list += name + "\n"

    embed = discord.Embed(
        title="Players Online:", 
        description=player_list,
        color=0x7aa660
    )

    embed.set_footer(text=f"Server IP: {server_ip}")
    await ctx.send(embed=embed)
    logsmaker.info(f"Command used. Author: {ctx.author}. Channel: {ctx.channel}. Command: players.")

# New help command
@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(
        title="Help menu", 
        color=0x7aa660
    )

    embed.add_field(name=f"{command_prefix}help", value="Displays this menu.", inline=False)
    embed.add_field(name=f"{command_prefix}echo", value="Test command. Answers \"Hello!\".", inline=False)
    embed.add_field(name=f"{command_prefix}status", value="Gives basic info about the server.", inline=False)
    embed.add_field(name=f"{command_prefix}ping", value="Gives the server's ping.", inline=False)
    embed.add_field(name=f"{command_prefix}players", value="Lists of all players online.", inline=False)

    embed.set_footer(text=f"Server IP: {server_ip}")
    await ctx.send(embed=embed)
    logsmaker.info(f"Command used. Author: {ctx.author}. Channel: {ctx.channel}. Command: help.")

# Detects need for help
@bot.event
async def on_message(message):
    if message.author != bot.user:
        if " help " in message.content or "aide " in message.content: 
            if " bot " in message.content: 
                ctx = await bot.get_context(message)
                await help(ctx)

    await bot.process_commands(message)

# Run the bot
bot.run(token)