#!/usr/bin/env python3
#coding=utf8

import discord
import psutil
from time import perf_counter
from assets.logger import writelog, startup_log
from assets.dbmanager import *
import commands

async def command_launcher(message: discord.Message, client: discord.Client) :
    cmd = str(message.content.split(' ', 1)[0])
    args = message.content.split()[2:]
    try :
        command = getattr(commands, cmd)
        await command()
    except (AttributeError) :
        await message.add_reaction("⁉️")
    return