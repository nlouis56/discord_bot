#!/usr/bin/env python3
#coding=utf8

from os import getenv, getpid, _exit
import discord
from random import choice
import psutil
from dotenv import load_dotenv
from utils import Utils
from embeds import help_message, permissions_error, git_repo, warning_stop_bot, make_embed, mention_startup
from tcp_latency import measure_latency

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

current = psutil.Process(getpid())

client = discord.Client()

#UTILS  ↑
###############################################################################
#COMMANDS  ↓


async def spam(message) :
    txt = ' '.join(message.content.split()[2:])
    qty = 0
    if (txt == "help") :
        await message.channel.send("spam <qty> <txt>")
        return
    try :
        qty = int(message.content.split()[1])
    except (ValueError) :
        await message.channel.send("c'est pas comme ça que ça s'utilise <:1Head:814062704355704853>\nps : si tu demande gentiment je peux te donner de l'aide")
        return
    if (qty > 10) :
        await message.channel.send("force pas trop non plus frérot")
        return
    elif (message.mentions) :
        await message.reply(f"jvais ping ta mère aussi")
        return
    i = 0
    for i in range (0, qty) :
        await message.channel.send(txt)
        i = i + 1

async def man_bash(message) :
    with open('bash.txt', encoding="utf8") as file :
        man = file.read()
        n = 1980
        for index in range(0, len(man), n):
            str = "```" + (man[index : index + n]) + "```"
            await message.channel.send(str)
            index = index  + n

async def say(message) :
    txt = ' '.join(message.content.split()[2:])
    try :
        n = int(message.content.split()[1])
    except (ValueError) :
        await message.channel.send("c'est pas comme ça que ça s'utilise <:1Head:814062704355704853>\nps : si tu demande gentiment je peux te donner de l'aide")
        return
    try :
        channel = client.get_channel(n)
        await channel.send(txt)
    except AttributeError :
        await message.channel.send("L'ID de channel est pas correcte apparemment")

async def ping(message) :
    if (message.author.bot) :
        await message.channel.send("sale bot de merde")
    else :
        await message.add_reaction("🖕")
        await message.channel.send(choice(utils.ping_response))

async def sys_load(message) :
    mem = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=None)
    if (mem > 50) :
        color = 0xfc5e03 ##rouge
    elif (mem > 40) :
        color = 0xfcad03 ##jaune-orangé
    elif (mem > 25) :
        color = 0xfcf403 ##jaune clair
    elif (mem > 10) :
        color = 0x03fcd7 ##bleu
    else :
        color = 0x94fc03 ##vert
    sysload = discord.Embed(title="Charge Système", description="", color=color)
    m = round(((current.memory_info().rss) / 1000000), 2)
    memusage = str(mem) + "\n(j'utilise actuellement " + str(m) + " MO de RAM)"
    sysload.add_field(name="RAM (%)", value=memusage)
    sysload.add_field(name="CPU (%)", value=cpu)
    sysload.set_footer(text="c'est pas une raison pour tout péter")
    await message.channel.send(embed=sysload)

async def list_servers(message) :
    server_list = discord.Embed(title="Liste des serveurs :")
    for guild in client.guilds:
        server_list.add_field(name=guild.name, value="id : " + str(guild.id), inline=False)
    await message.channel.send(embed=server_list)

async def killbot(message) :
    if utils.is_su(message.author.mention) :
        await message.channel.send("c'est la fin de moi, ciao les gens")
        print(">killbot received, ending program")
        for c in utils.channels :
            chan = client.get_channel(int(c))
            await chan.send(embed=warning_stop_bot)
        _exit(0)
    else :
        await message.channel.send(embed=permissions_error)
        await message.channel.send("sal fou mdrr")

async def ping_test(message) :
    await message.add_reaction("📡")
    ping = measure_latency(host='discord.gg', runs=5, human_output=False)
    avg = sum(ping) / len(ping)
    avg = round(avg, 2)
    if (avg > 50) :
        color = 0xfc5e03 ##rouge
    elif (avg > 40) :
        color = 0xfcad03 ##jaune-orangé
    elif (avg > 25) :
        color = 0xfcf403 ##jaune clair
    elif (avg > 10) :
        color = 0x03fcd7 ##bleu
    else :
        color = 0x94fc03 ##vert
    await message.channel.send(embed=make_embed("Ping avec discord.gg :", str(avg) +  " ms", color=color))


#COMMANDS  ↑
###############################################################################
#CHATROOM  ↓


async def distribute_message(message) :
    field = "〰️ 〰️ 〰️ 〰️"
    msg_embed = discord.Embed(title="Serveur : " + message.guild.name)
    msg_embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    if message.reference :
        replied_to = message.reference
        msg = await message.channel.fetch_message(replied_to.message_id)
        if msg.embeds :
            emb = msg.embeds[0]
            emb_dct = emb.to_dict()
            try :
                emb_fields = emb_dct["fields"]
                if len(emb_fields) > 1 :
                    msg_embed.add_field(name="répond à :", value=str(emb_dct["author"]["name"]) + "\n" + str(emb_dct["fields"][1]["value"]), inline=False)
                else :
                    msg_embed.add_field(name="répond à :", value=str(emb_dct["author"]["name"]) + "\n" + str(emb_dct["fields"][0]["value"]), inline=False)
            except KeyError :
                msg_embed.add_field(name="répond à :", value=str(msg.author.display_name) + "\n", inline=False)
        else :
            msg_embed.add_field(name="répond à :", value=str(msg.author.display_name) + "\n" + str(msg.content), inline=False)
        field = "message :"
    if message.attachments :
        msg_embed.set_image(url=message.attachments[0].url)
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
            await say(message)
    elif cmd == ">killbot" :               #KILLBOT
        await killbot(message)
    elif cmd == ">infosys" :               #INFOSYS
        await sys_load(message)
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
        await list_servers(message)
    elif cmd == ">ping" :                  #PING
        await ping_test(message)
    elif cmd == ">startup" :               #STARTUP
        await startup(message)
    else :
        await message.add_reaction("⁉️")

@client.event
async def on_ready():
    print(f"{client.user} est connecté à Discord !\nserveurs rejoints:")
    for guild in client.guilds:
        print(f"{guild.name} - id :{guild.id}")

@client.event
async def on_message(message) :
    await message_analyzer(message)
    if client.user.mentioned_in(message) :
        await ping(message)
    if message.content and message.content[0] == '>' :
        await commands_manager(message)

def main() :
    global utils
    utils = Utils()
    client.run(TOKEN)

if __name__ == "__main__" :
    main()