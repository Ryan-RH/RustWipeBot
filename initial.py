import discord
import aiohttp
import asyncio
import pytz
from datetime import datetime, timedelta
from discord.ext import commands

client = commands.Bot(command_prefix="?", intents=discord.Intents.all())
channel_id = 0

# Time calculation
def hoursAgo(server_data):
    last_wiped = int((datetime.now(pytz.utc) - datetime.strptime(server_data['data']['attributes']['details']['rust_last_wipe'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.UTC)).total_seconds()/3600)
    if last_wiped < 1:
        return ("Less than an hour ago")
    elif last_wiped == 1:
        return ("1 hour ago")
    else:
        return (str(last_wiped) + " hours ago")

# Embed Interface for Server Wipe
def createEmbed(server_data):
    population = str(server_data['data']['attributes']['players'])+ "/" + str(server_data['data']['attributes']['maxPlayers'])
    ip = server_data['data']['attributes']['ip'] + ":" + str(server_data['data']['attributes']['port'])
    time_difference = hoursAgo(server_data)
    embed = discord.Embed(
        title="Just Wiped!",
        description= ("ID: " + server_data['data']['id']),
        color=discord.Color.red()
        )
    embed.add_field(name=server_data['data']['attributes']['name'],
                    value="Population: \u2002" + population + "\nIP:\u2002\u2002\u2002\u2002\u2002\u2002\u2002\u2002\u2002" + ip+ "\nLast wipe: \u2002\u2002" + time_difference,
                    inline= False)
    return embed

# Grab Server Data
async def serverGrab(serverid):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.battlemetrics.com/servers/" + serverid) as response:
            return (await response.json())

async def purge(channel):
    async for message in channel.history(limit=None):
        await message.delete()
        await asyncio.sleep(2)

# Obtain Added Server IDs
with open('serverids.txt', 'r') as serveridfile:
    serverinfo = serveridfile.readlines()
serverinfo = [[line.strip()] for line in serverinfo]

@client.event
async def on_ready():
    # Extends Array into 2D with initial Last Wipe information
    print("Collecting Server Information...")
    for index, content in enumerate(serverinfo):
        try:
            server_data = await serverGrab(content[0])
            serverinfo[index].append(server_data['data']['attributes']['details']['rust_last_wipe'])
            serverinfo[index].append(server_data['data']['attributes']['name'])
        except:
            print("Failed to obtain data - Exceeded 60 API requests within 60 seconds.")
    print("Done.")
    initial_date = (datetime.now(pytz.utc)).date()
    today_wipe = []
    channel = client.get_channel(channel_id)
    await purge(channel)
    
    # Wipe Checker
    cycle = 1
    while True:
        if (datetime.now(pytz.utc)).date() != initial_date:
            today_wipe = []
            await purge(channel)
            initial_date = (datetime.now(pytz.utc)).date()
        print("Cycling through servers... [", cycle, "]")
        for content in serverinfo:
            server_data = await serverGrab(content[0])
            new_last_wipe = server_data['data']['attributes']['details']['rust_last_wipe']
            if new_last_wipe != content[1]:
                print("Wiped!")
                content[1] = new_last_wipe
                content[2] = server_data['data']['attributes']['name']
                today_wipe.append(content[0])
                newWipe = createEmbed(server_data)
                await channel.send(embed=newWipe)
            await asyncio.sleep(2)
        index = -1
        async for message in channel.history(limit=None):
            if message.embeds:
                index+=1
                updated = createEmbed(await serverGrab(today_wipe[len(today_wipe)-1-index]))
                await message.edit(embed=updated)
        cycle+=1
        

# ?add command for adding new server ID
@client.command()
async def add(ctx, serverid=None):
    if serverid is None:
        await ctx.send("Please add a server ID after the use of ?add.")
    else:
        # Check Duplicate
        for content in serverinfo:
            if serverid == content[0]:
                await ctx.send("Server ID already exists")
                return
        # Verify Rust Server, append to notepad and array
        try:
            server_data = await serverGrab(serverid)
            last_wipe = server_data['data']['attributes']['details']['rust_last_wipe']
            name = server_data['data']['attributes']['name']
            with open('serverids.txt', 'a') as serveridfile:
                serveridfile.write(serverid + "\n")
            serverinfo.append([serverid, last_wipe, name])
            await ctx.send("Server added.")
        except:
            await ctx.send("Server ID supplied is not a rust server, please verify and try again.")

# ?remove command for removing a server ID
@client.command()
async def remove(ctx, serverid=None):
    if serverid is None:
        await ctx.send("Please add a server ID after the use of ?remove.")
    else:
        for content in serverinfo:
            if serverid == content[0]:
                await ctx.send("Server removed.")
                serverinfo.remove(content)
                with open('serverids.txt', 'w') as serveridfile:
                    for element in serverinfo:
                        serveridfile.write(element[0] + "\n")
                return
        await ctx.send("Server ID not found.")

async def embedServerList(serverids, servernames):
    embed = discord.Embed(title="Servers", color=discord.Color.green())
    embed.add_field(name="ID", value=serverids, inline=True)
    embed.add_field(name="Name", value=servernames, inline=True)
    return embed

def shorten_string(text):
    if len(text) <= 59:
        return text
    else:
        return text[:56] + "..."

# ?serverlist command for showing all servers
@client.command()
async def serverlist(ctx):
    serverlistinfo = serverinfo
    final = 0
    while final == 0:
        serverids = ""
        servernames = ""
        for index, content in enumerate(serverlistinfo):
            if len(serverids + content[0]) < 1024 and len(servernames + shorten_string(content[2])) < 1024:
                serverids += content[0]
                servernames += shorten_string(content[2])
                if content != serverinfo[-1]:
                    serverids += "\n"
                    servernames += "\n"
                else:
                    final = 1
                    await ctx.send(embed=(await embedServerList(serverids, servernames)))
                    break
            else:
                await ctx.send(embed=(await embedServerList(serverids, servernames)))
                serverlistinfo = serverlistinfo[index:]
                break
                        
            
client.run("x")
