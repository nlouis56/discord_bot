
import discord
import psutil
import urllib, re
from os import _exit
from random import choice
from utils import Utils
from tcp_latency import measure_latency
from embeds import permissions_error, warning_stop_bot, make_embed


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

async def say(message, client) :
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

async def ping(message, utils) :
    if (message.author.bot) :
        await message.channel.send("sale bot de merde")
        return
    for c in utils.channels :
        if c == str(message.channel.id) :
            return
    else :
        await message.add_reaction("🖕")
        await message.channel.send(choice(utils.ping_response))

async def sys_load(message, current) :
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

async def list_servers(message, client) :
    server_list = discord.Embed(title="Liste des serveurs :")
    for guild in client.guilds:
        server_list.add_field(name=guild.name, value="id : " + str(guild.id), inline=False)
    await message.channel.send(embed=server_list)

async def killbot(message, utils, client) :
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

async def decompose(message) :
    try :
        id = int(message.content.split()[1])
    except (ValueError) :
        await message.channel.send("c'est pas comme ça que ça s'utilise <:1Head:814062704355704853>\nps : si tu demande gentiment je peux te donner de l'aide")
        return
    msg = await message.channel.fetch_message(id)
    if msg.embeds :
        emb = msg.embeds[0]
        emb_dct = emb.to_dict()
        await message.channel.send(str(emb_dct))