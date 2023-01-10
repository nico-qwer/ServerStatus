# Imports
# discord.py for discord API
import discord
from discord import app_commands
from discord.ext import commands

# mcstatus for server monitoring
from mcstatus import JavaServer

# custom library for log file
import logsmaker


# Read values from txt files
with open('dev_token.txt', 'r') as token_file:
    token = token_file.readline()
with open('serverIP.txt', 'r') as IP_file:
    server_ip = IP_file.readline()
with open('botOwnerId.txt', 'r') as owner_file:
    ownerId = owner_file.readline()


# Setup bot
intents = discord.Intents.all()
command_prefix = "$"
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.remove_command("help")

# Setup mcstatus
server = JavaServer.lookup(server_ip)


# Warn bot owner that mc server is offline
async def offline_notif(inter):
    user = await bot.fetch_user(ownerId)

    await inter.edit_original_response(f"The server did not answer, it's probably offline. I will be contacting {user.name} so he can fix this.")
    await user.send("Minecraft server is offline!!")
    logsmaker.error("Server offline.")


# commands
@bot.tree.command(name="echo")
async def echo(inter: discord.Interaction):
    await inter.response.send_message("Hello!")
    logsmaker.info(f"Command used. Author: {inter.user.name}. Channel: {inter.channel}. Command: echo.")

@bot.tree.command(name="status")
async def status(inter: discord.Interaction):
    await inter.response.send_message("Waiting for server...")
    try:
        status = server.status()
    except TimeoutError:
        await offline_notif(inter)
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

    await inter.edit_original_response(content="", embed=embed)
    logsmaker.info(f"Command used. Author: {inter.user.name}. Channel: {inter.channel}. Command: status.")

@bot.tree.command(name="ping")
async def ping(inter: discord.Interaction):
    await inter.response.send_message("Waiting for server...")
    try:
        latency = server.ping()
    except TimeoutError:
        await offline_notif(inter)
        return

    await inter.edit_original_response(content=f"The server replied in {round(latency, 2)} ms")
    logsmaker.info(f"Command used. Author: {inter.user.name}. Channel: {inter.channel}. Command: ping.")

@bot.tree.command(name="players")
async def players(inter: discord.Interaction):
    await inter.response.send_message("Waiting for server...")
    try:
        query = server.query()
    except TimeoutError:
        await offline_notif(inter)
        return

    if query.players.names == []:
        await inter.edit_original_response(content="There are no players online.")
        logsmaker.info(f"Command used. Author: {inter.user.name}. Channel: {inter.channel}. Command: players.")
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
    
    await inter.edit_original_response(content="", embed=embed)

    logsmaker.info(f"Command used. Author: {inter.user.name}. Channel: {inter.channel}. Command: players.")


# Slash command syncing
@bot.command()
async def sync(ctx: commands.Context):
    if (str(ctx.author.id) != ownerId):
        await ctx.send("Only the owner of the bot can sync slash commands.")
        return

    try:
        synced = await bot.tree.sync()

        await ctx.send(f"Synced {len(synced)} command(s)")
        logsmaker.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        await ctx.send(e)
        logsmaker.error(f"Slash command syncing error: {e}")


# When bot is ready
@bot.event
async def on_ready():
    print(f"Bot is online. Logged in as {bot.user.name}.")
    logsmaker.info("Bot is back online.", "\n")


# Run the bot
bot.run(token)