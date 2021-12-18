#!/usr/bin/env python3
#coding=utf8

import discord
import psutil
from time import perf_counter
from os import getenv, getpid
from dotenv import load_dotenv
from assets.logger import writelog, startup_log
from assets.dbmanager import *

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN_TEST')

PID = psutil.Process(getpid())
PC_START = 0
PC_STOP = 0

COUNT = 0

client = discord.Client()

sqlconfig = {
    "host" : getenv('SQL_HOST'),
    "user" : getenv('SQL_USER'),
    "password" : getenv('SQL_PASSWORD')
}

def performance_logger() -> None :
    global COUNT
    COUNT = COUNT + 1
    if COUNT >= 5 :
        writelog(perfreport=True)
        COUNT = 0

@client.event
async def on_message(message: discord.Message) -> None :
    if message.author == client.user :
        return
    performance_logger()
    update_member(member=message.author)

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent) -> None :
    guild = client.get_guild(payload.guild_id)
    if payload.member == client.user :
        return
    role = check_reaction_role(guild, payload.message_id, payload.emoji)
    if role is not None :
        await payload.member.add_roles(role)
        writelog(title="REACTION ROLES", message=f"Role {role.name} added to {payload.member.name} in {guild.name}")

@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent) -> None :
    guild = client.get_guild(payload.guild_id)
    member = await guild.fetch_member(int(payload.user_id))
    if member == client.user :
        return
    role = check_reaction_role(guild, payload.message_id, payload.emoji)
    if role is not None :
        await member.remove_roles(role) # !! NOT WORKING !! AttributeError: 'NoneType' object has no attribute 'remove_roles'
        writelog(title="REACTION ROLES", message=f"Role {role.name} removed from {member.name} in {guild.name}")

@client.event
async def on_guild_join(guild: discord.Guild) -> None :
    print (f"{client.user} joined {guild.name}")
    register_new_server(guild)

@client.event
async def on_guild_remove(guild: discord.Guild) -> None :
    print (f"{client.user} left {guild.name}")
    remove_server(guild)

@client.event
async def on_ready() -> None :
    global PC_STOP, PC_START
    update_servers(client)
    PC_STOP = perf_counter()
    writelog(title="STARTUP", message=f"Startup completed in {PC_STOP - PC_START:0.4f} seconds")
    print(f"Startup completed in {PC_STOP - PC_START:0.4f} seconds")

def main() :
    global PC_START
    PC_START = perf_counter()
    startup_log()
    if not test_connection() :
        writelog(title="STARTUP", message="Could not connect to the main database ! Missing .env file ?", error=True)
        print("ERROR ! Could not connect to the main database ! Missing .env file ?")
        return
    writelog(title="STARTUP", message="Bot started, client.run to be executed")
    client.run(TOKEN)

if __name__ == "__main__" :
    main()