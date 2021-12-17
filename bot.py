#!/usr/bin/env python3
#coding=utf8

import discord
import psutil
from time import perf_counter
from os import getenv, getpid
from dotenv import load_dotenv
from logger import writelog, startup_log
from dbmanager import *

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
async def on_message(message) -> None :
    if message.author == client.user :
        return
    performance_logger()
    update_member(sqlconfig, member=message.author)

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent) :
    writelog(title="REACTION", message="Reaction received, looking for match with reaction roles")
    guild = client.get_guild(payload.guild_id)
    role = check_reaction_role(sqlconfig, guild, payload.message_id, payload.emoji)
    if role is not None :
        await payload.member.add_roles(role)
        writelog(title="REACTION ROLES", message=f"Role {role.name} added to {payload.member.name} in {guild.name}")
    else :
        writelog(title="REACTION", message="Role could not be fetched")

@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent) :
    writelog(title="REACTION", message="Reaction removed, looking for match with reaction roles")
    guild = client.get_guild(payload.guild_id)
    role = check_reaction_role(sqlconfig, guild, payload.message_id, payload.emoji)
    member = await guild.fetch_member(int(payload.user_id))
    if role is not None :
        await member.remove_roles(role) # !! NOT WORKING !! AttributeError: 'NoneType' object has no attribute 'remove_roles'
        writelog(title="REACTION ROLES", message=f"Role {role.name} removed from {member.name} in {guild.name}")
    else :
        writelog(title="REACTION", message="Role could not be fetched")

@client.event
async def on_guild_join(guild) :
    print (f"{client.user} joined {guild.name}")
    register_new_server(sqlconfig, guild)

@client.event
async def on_guild_remove(guild) :
    print (f"{client.user} left {guild.name}")
    remove_server(sqlconfig, guild)

@client.event
async def on_ready() -> None :
    global PC_STOP, PC_START
    update_servers(sqlconfig, client)
    PC_STOP = perf_counter()
    writelog(title="STARTUP", message=f"Startup completed in {PC_STOP - PC_START:0.4f} seconds")
    print(f"Startup completed in {PC_STOP - PC_START:0.4f} seconds")

def main() :
    global PC_START
    PC_START = perf_counter()
    if not test_connection(sqlconfig) :
        writelog(title="STARTUP", message="Could not connect to the main database !", error=True)
        print("ERROR ! Could not connect to the main database !")
        return
    else :
        startup_log()
        writelog(title="STARTUP", message="Bot started, client.run to be executed")
        client.run(TOKEN)

if __name__ == "__main__" :
    main()