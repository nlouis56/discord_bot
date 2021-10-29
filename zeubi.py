#!/usr/bin/env python3
#coding=utf8

from os import getenv, getpid, path, _exit
import discord
from random import choice
import psutil
from dotenv import load_dotenv
from utils import Utils
from embeds import help_message, permissions_error, git_repo, mention_startup
from commands import spam, man_bash, say, ping, sys_load, list_servers, killbot, ping_test, decompose

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

current = psutil.Process(getpid())

client = discord.Client()

#UTILS  ↑
###############################################################################
#CHATROOM  ↓


async def distribute_message(message) :
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

async def add_channel(message) :
    chan = message.channel.id
    if bool(utils.channels) :
        is_added = False
        for c in utils.channels :
            if c == str(chan) :
                is_added = True
                await message.channel.send("Le channel \"" + message.channel.name + "\" est déjà enregistré")
                await message.add_reaction("⚠️")
                break
        if not is_added :
            with open(utils.chatroom_channels, "a", encoding="utf8") as fchr :
                    fchr.write(str(chan) + "\n")
            utils.refresh()
            await message.add_reaction("✅")
    else :
        print("empty file")
        with open(utils.chatroom_channels, "a", encoding="utf8") as fchr :
            fchr.write(str(chan) + "\n")
        utils.refresh()
        await message.add_reaction("✅")

async def rmchannel(message) :
    with open(utils.chatroom_channels, "r") as f:
        lines = f.readlines()
    with open(utils.chatroom_channels, "w") as f:
        for line in lines:
            if line.strip("\n") != str(message.channel.id):
                f.write(line)
    utils.refresh()
    await message.add_reaction("✅")

async def startup(message) :
    if utils.is_su(message.author.mention) :
        for c in utils.channels :
            chan = client.get_channel(int(c))
            await chan.send(embed=mention_startup)
    else :
        await message.channel.send(embed=permissions_error)

async def message_analyzer(message) :
    await add_reaction(message)
    for c in utils.channels :
        if c == str(message.channel.id) :
            await distribute_message(message)
            return

#CHATROOM  ↑
###############################################################################
#AUTOMATIC REACTIONS  ↓

async def add_reaction(message) :
    for react in utils.reactions :
        if react in message.content :
                em = choice(utils.reactions[react])
                await message.add_reaction(em)    

#AUTOMATIC REACTIONS  ↑
###############################################################################
#EVENTS & COMMAND MANAGER ↓

async def commands_manager(message) :
    cmd = str(message.content.split()[0])
    if cmd == ">test" :                     #TEST
        if utils.is_su(message.author.mention) :
            await message.channel.send("tester c'est douter")
        else :
            await message.channel.send(embed=permissions_error)
    elif cmd == ">help" :                   #HELP
        help_message.set_thumbnail(url=message.guild.icon_url)
        await message.channel.send(embed=help_message)
    elif cmd == ">invite" :                 #INVITE
        await message.channel.send("voilà le lien d'invitation espèce de bg : \
            https://discord.com/api/oauth2/authorize?client_id=890884345018069032&permissions=8&scope=bot")
    elif cmd == ">spam" :                   #SPAM
        await spam(message)
    elif cmd == ">say" :                    #SAY
        if (message.author.bot) :
            message.channel.send("non mdr")
        else :
            await say(message, client)
    elif cmd == ">killbot" :               #KILLBOT
        await killbot(message, utils, client)
    elif cmd == ">infosys" :               #INFOSYS
        await sys_load(message, current)
    elif cmd == ">man_bash" :              #MAN_BASH
        await man_bash(message)
    elif cmd == ">reload_assets" :         #RELOAD_ASSETS
        if utils.is_su(message.author.mention) :
            utils.refresh()
            await message.add_reaction("✅")
        else :
            await message.channel.send(embed=permissions_error)
    elif cmd == ">dump" :                  #DUMP
        string = "```" + message.content + "```"
        await message.channel.send(string)
    elif cmd == ">addchannel" :            #ADDCHANNEL
        await add_channel(message)
    elif cmd == ">rmchannel" :             #RMCHANNEL
        await rmchannel(message)
    elif cmd == ">rick" :                  #RICK
        await message.channel.send("https://tenor.com/view/rick-astley-never-gonna-give-you-up-cry-for-help-pwl-stock-aitken-waterman-gif-17671973")
    elif cmd == ">git" :                   #GIT
        await message.channel.send(embed=git_repo)
    elif cmd == ">list_servers" :          #LIST_SERVERS
        await list_servers(message, client)
    elif cmd == ">ping" :                  #PING
        await ping_test(message)
    elif cmd == ">startup" :               #STARTUP
        await startup(message)
    elif cmd == ">decompose" :
        await decompose(message)
    else :
        await message.add_reaction("⁉️")

@client.event
async def on_ready():
    print(f"{client.user} is connected to Discord !\n")
    for guild in client.guilds:
        print(f"{guild.name} - id :{guild.id}")

@client.event
async def on_message(message) :
    await message_analyzer(message)
    if client.user.mentioned_in(message) :
        await ping(message, utils)
    if message.content and message.content[0] == '>' :
        await commands_manager(message)

def main() :
    global utils
    if path.isfile("./settings.json") :
        utils = Utils()
        client.run(TOKEN)
    else :
        print("Error ! settings.json is not present ! Aborting.")
        _exit(-1)

if __name__ == "__main__" :
    main()