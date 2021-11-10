
import discord
import psutil
from os import _exit
from random import choice
from utils import Utils
from tcp_latency import measure_latency
from embeds import permissions_error, stopping_message, make_embed, startup_message, help_message, git_repo

async def help(message, client, current, utils) :
    serv_lang = utils.server_lang(message.guild.id)
    help_message[serv_lang].set_thumbnail(url=message.guild.icon_url)
    await message.channel.send(embed=help_message[serv_lang])

async def spam(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
    txt = ' '.join(message.content.split()[2:])
    qty = 0
    if (txt == "help") :
        await message.channel.send("spam <qty> <txt>")
        return
    try :
        qty = int(message.content.split()[1])
    except (ValueError) :
        await message.channel.send(utils.lang[lang]["usage"])
        return
    if (qty > 10) :
        await message.channel.send(utils.lang[lang]["spam_cooldown"])
        return
    elif (message.mentions) :
        await message.reply(utils.lang[lang]["spam_tag"])
        return
    i = 0
    for i in range (0, qty) :
        await message.channel.send(txt)
        i = i + 1

async def man_bash(message, client, current, utils) :
    with open('bash.txt', encoding="utf8") as file :
        man = file.read()
        n = 1980
        for index in range(0, len(man), n):
            str = "```" + (man[index : index + n]) + "```"
            await message.channel.send(str)
            index = index  + n

async def say(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
    txt = ' '.join(message.content.split()[2:])
    try :
        n = int(message.content.split()[1])
    except (ValueError) :
        await message.channel.send(utils.lang[lang]["usage"])
        return
    try :
        channel = client.get_channel(n)
        await channel.send(txt)
    except AttributeError :
        await message.channel.send(utils.lang[lang]["chid_error"])

async def ping_rep(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
    if (message.author.bot) :
        await message.channel.send(utils.lang[lang]["bot_reply"])
        return
    for c in utils.channels :
        if c == str(message.channel.id) :
            return
    else :
        await message.add_reaction("🖕")
        await message.channel.send(choice(utils.ping_response))

async def infosys(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
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
    sysload = discord.Embed(title=utils.lang[lang]["sysload_title"], description="", color=color)
    m = round(((current.memory_info().rss) / 1000000), 2)
    memusage = str(mem) + "\n" + utils.lang[lang]["sysload_self"] + str(m) + " MB RAM)"
    sysload.add_field(name="RAM (%)", value=memusage)
    sysload.add_field(name="CPU (%)", value=cpu)
    await message.channel.send(embed=sysload)

async def list_servers(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
    server_list = discord.Embed(title=utils.lang[lang]["server_list"])
    for guild in client.guilds:
        server_list.add_field(name=guild.name, value="id : " + str(guild.id), inline=False)
    await message.channel.send(embed=server_list)

async def killbot(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
    if utils.is_su(message.author.mention) :
        await message.channel.send(utils.lang[lang]["killbot"])
        print(">killbot received, ending program")
        for c in utils.channels :
            chan = client.get_channel(int(c))
            lang = utils.server_lang(chan.guild.id)
            await chan.send(embed=stopping_message[lang])
        _exit(0)
    else :
        await message.channel.send(embed=permissions_error[lang])

async def ping(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
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
    await message.channel.send(embed=make_embed(utils.lang[lang]["ping"], str(avg) +  " ms", color=color))

async def addchannel(message, client, current, utils) :
    utils = Utils()
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

async def rmchannel(message, client, current, utils) :
    utils = Utils()
    with open(utils.chatroom_channels, "r") as f:
        lines = f.readlines()
    with open(utils.chatroom_channels, "w") as f:
        for line in lines:
            if line.strip("\n") != str(message.channel.id):
                f.write(line)
    utils.refresh()
    await message.add_reaction("✅")

async def startup(message, client, current, utils) :
    utils = Utils()
    if utils.is_su(message.author.mention) :
        for c in utils.channels :
            chan = client.get_channel(int(c))
            lang = utils.server_lang(chan.guild.id)
            await chan.send(embed=startup_message[lang])
    else :
        lang = utils.server_lang(message.guild.id)
        await message.channel.send(embed=permissions_error[lang])

async def decompose(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
    try :
        id = int(message.content.split()[1])
    except (ValueError) :
        await message.channel.send(utils.lang[lang]["usage"])
        return
    msg = await message.channel.fetch_message(id)
    if msg.embeds :
        emb = msg.embeds[0]
        emb_dct = emb.to_dict()
        await message.channel.send(str(emb_dct))

async def setup_en(message, client, current, utils) :
    srv = message.guild.id
    if bool(utils.en_servers) :
        is_added = False
        for c in utils.en_servers :
            if c == str(srv) :
                is_added = True
                await message.channel.send("The server \"" + message.guild.name + "\" is already set up")
                await message.add_reaction("⚠️")
                break
        if not is_added :
            with open(utils.en_servers_file, "a", encoding="utf8") as fchr :
                    fchr.write(str(srv) + "\n")
            utils.refresh()
            await message.add_reaction("✅")
    else :
        print("empty file")
        with open(utils.en_servers_file, "a", encoding="utf8") as fchr :
            fchr.write(str(srv) + "\n")
        utils.refresh()
        await message.add_reaction("✅")
    return

async def setup_fr(message, client, current, utils) :
    with open(utils.en_servers_file, "r") as f:
        lines = f.readlines()
    with open(utils.en_servers_file, "w") as f:
        for line in lines:
            if line.strip("\n") != str(message.guild.id):
                f.write(line)
    utils.refresh()
    await message.add_reaction("✅")

async def git(message, client, current, utils) :
    await message.channel.send(embed=git_repo)

async def dump(message, client, current, utils) :
    string = "```" + message.content + "```"
    await message.channel.send(string)

async def reload_assets(message, client, current, utils) :
    if utils.is_su(message.author.mention) :
            utils.refresh()
            await message.add_reaction("✅")

async def invite(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
    await message.channel.send(utils.lang[lang]["invite"] + "https://discord.com/api/oauth2/authorize?client_id=890884345018069032&permissions=534559321424&scope=bot")

async def test(message, client, current, utils) :
    lang = utils.server_lang(message.guild.id)
    if utils.is_su(message.author.mention) :
        await message.channel.send(utils.lang[lang]["test"])
    else :
        await message.channel.send(embed=permissions_error[lang])

async def rick(message, client, current, utils) :
    await message.channel.send("https://tenor.com/view/rick-astley-never-gonna-give-you-up-cry-for-help-pwl-stock-aitken-waterman-gif-17671973")

