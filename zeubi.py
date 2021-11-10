#!/usr/bin/env python3
#coding=utf8

from os import getenv, getpid, path, _exit
import discord
from random import choice
import psutil
from dotenv import load_dotenv
from utils import Utils
from embeds import help_message, permissions_error, git_repo
from commands import ping_rep
import commands

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

current = psutil.Process(getpid())

client = discord.Client()

#UTILS  ↑
###############################################################################
#CHATROOM  ↓


async def distribute_message(message) :
    utils = Utils()
    lang = utils.server_lang(message.guild.id)
    field = "〰️ 〰️ 〰️ 〰️"
    msg_embed = discord.Embed(title="Serveur : " + message.guild.name)
    msg_embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    lnk = None

    if message.reference :
        replied_to = message.reference
        msg = await message.channel.fetch_message(replied_to.message_id)
        if msg.embeds :
            emb = msg.embeds[0]
            emb_dct = emb.to_dict()
            try :
                emb_fields = emb_dct["fields"]
                if len(emb_fields) > 1 :
                    msg_embed.add_field(name="répond à :", value="***" + str(emb_dct["author"]["name"]) + "***" + "\n" + str(emb_dct["fields"][1]["value"]), inline=False)
                else :
                    msg_embed.add_field(name="répond à :", value="***" + str(emb_dct["author"]["name"]) + "***" + "\n" + str(emb_dct["fields"][0]["value"]), inline=False)
            except KeyError :
                msg_embed.add_field(name="répond à :", value="***" + str(msg.author.display_name) + "***" + "\n", inline=False)
        else :
            msg_embed.add_field(name="répond à :", value="***" + str(msg.author.display_name) + "***" + "\n" + str(msg.content), inline=False)
        field = "message :"
    if message.attachments :
        msg_embed.set_image(url=message.attachments[0].url)
    if message.content.startswith("https://tenor.com/") :
        lnk = str(message.content.split()[0])
    if message.content :
        if len(message.content) >= 1024 :
            await message.reply("un message en embed ne peut pas être plus long que 1024 caractères")
            msg_embed.add_field(name="<texte trop long>", value="limite de 1024 caractères pour les messages dans ce salon")
        else :
            msg_embed.add_field(name=field + "〰️\n", value=message.content, inline=False)
    for c in utils.channels :
        if c != str(message.channel.id) :
            if message.author.id == client.user.id and message.embeds :
                return
            else :
                chan = client.get_channel(int(c))
                await chan.send(embed=msg_embed)
                if lnk :
                    await chan.send(lnk)

async def message_analyzer(message) :
    utils = Utils()
    await add_reaction(message)
    for c in utils.channels :
        if c == str(message.channel.id) :
            await distribute_message(message)
            return

#CHATROOM  ↑
###############################################################################
#AUTOMATIC REACTIONS  ↓

async def add_reaction(message) :
    utils = Utils()
    for react in utils.reactions :
        if react in message.content :
                em = choice(utils.reactions[react])
                await message.add_reaction(em)

#AUTOMATIC REACTIONS  ↑
###############################################################################
#EVENTS & MAIN ↓

@client.event
async def on_ready():
    print(f"{client.user} is connected to Discord !\n")
    for guild in client.guilds:
        print(f"{guild.name} - id :{guild.id}")

@client.event
async def on_message(message) :
    utils = Utils()
    await message_analyzer(message)
    if client.user.mentioned_in(message) :
        await ping_rep(message, client, current, utils)
    if message.content and message.content[0] == '>' :
        cmd = str(message.content.split()[0])
        cmd = cmd[1:]
        try :
            command = getattr(commands, cmd)
            await command(message,client, current, utils)
        except (AttributeError) :
            await message.add_reaction("⁉️")
        #await commands_manager(message)
    del utils

def main() :
    if path.isfile("./settings.json") :
        client.run(TOKEN)
    else :
        print("Error ! settings.json is not present ! Aborting.")
        _exit(-1)

if __name__ == "__main__" :
    main()