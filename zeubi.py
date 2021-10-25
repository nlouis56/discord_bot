#!/usr/bin/env python3
#coding=utf8

import os
import discord
import random
import json
import psutil
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

help_message = discord.Embed(title="L'aide de zeubi", description="vraiment joli ce truc")
help_message.add_field(name="Commandes :", value="\n>spam <quantité> <mot>\n\
    >test\n\
        >invite\n\
            >say <channel id> <message>\n\
                >infosys\n\
                    >man_bash\n\
                        >dump")
help_message.add_field(name="Perms Zone :", value=">killbot\n>reload_assets")
help_message.set_footer(text="et puis voilà hein faut pas trop en demander non plus")

permissions_error = discord.Embed(title="Erreur !", description="", color=0xFC0303)
permissions_error.add_field(name="T'as pas les perms", value="Erreur de permissions, tu ne peux pas éxecuter cette commande")
permissions_error.set_footer(text="cheh mdr")

current = psutil.Process(os.getpid())

client = discord.Client()

def load_assets() :
    global ping_response, superusers, reactions
    with open('settings.json', encoding='utf-8') as f:
        data = json.load(f)
    responses = data["dialogs"]["responses"]
    superusers = data["userinfo"]["superusers"]
    reactions = data["autoresponses"]
    with open(responses, encoding="utf8") as fresp :
        ping_response = fresp.read().splitlines()

def perms_check(user_id) -> bool:
    if user_id in superusers :
        return (True)
    else :
        return (False)


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
        await message.channel.send("c'est pas comme ça que ça s'utilise <:1Head:814062704355704853>\n\
                ps : si tu demande gentiment je peux te donner de l'aide")
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
        await message.channel.send(random.choice(ping_response))

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

async def commands_manager(message) :
    if message.content.startswith(">test") :
        if perms_check(message.author.mention) :
            await message.channel.send("tester c'est douter")
        else :
            await message.channel.send(embed=permissions_error)
    elif message.content.startswith(">help") :
        help_message.set_thumbnail(url=message.guild.icon_url)
        await message.channel.send(embed=help_message)
    elif message.content.startswith(">invite") :
        await message.channel.send("voilà le lien d'invitation espèce de bg : \
            https://discord.com/api/oauth2/authorize?client_id=890884345018069032&permissions=8&scope=bot")
    elif message.content.startswith(">spam") :
        await spam(message)
    elif message.content.startswith(">say") :
        await say(message)
    elif message.content.startswith(">killbot") :
        if perms_check(message.author.mention) :
            await message.channel.send("c'est la fin de moi, ciao les gens")
            print(">killbot received, ending program")
            os._exit(0)
        else :
            await message.channel.send(embed=permissions_error)
            await message.channel.send("sal fou mdrr")
    elif message.content.startswith(">infosys") :
        await sys_load(message)
    elif message.content.startswith(">man_bash") :
        await man_bash(message)
    elif message.content.startswith(">reload_assets") :
        if perms_check(message.author.mention) :
            load_assets()
            await message.add_reaction("✅")
        else :
            await message.channel.send(embed=permissions_error)
    elif message.content.startswith(">dump") :
        str = "```" + message.content + "```"
        await message.channel.send(str)


#COMMANDS  ↑
###############################################################################
#AUTOMATIC REACTIONS  ↓

async def add_reaction(message) :
    for react in reactions :
        if react in message.content :
                em = random.choice(reactions[react])
                await message.add_reaction(em)

async def message_analyzer(message) :
    await add_reaction(message)


#AUTOMATIC REACTIONS  ↑
###############################################################################
#EVENTS  ↓


@client.event
async def on_ready():
    print(f"{client.user} est connecté à Discord !\nserveurs rejoints:")
    for guild in client.guilds:
        print(f"{guild.name} - id :{guild.id}")
    load_assets()    

@client.event
async def on_message(message) :
    if client.user.mentioned_in(message) :
        await ping(message)
    if bool(message.content) and message.content[0] == '>' :
        await commands_manager(message)
    else :
        await message_analyzer(message)

client.run(TOKEN)