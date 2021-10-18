#!/usr/bin/env python3
#coding=utf8

import os
import discord
import random
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

with open('settings.json') as f:
    data = json.load(f)
responses = data["dialogs"]["responses"]
superusers = data["userinfo"]["superusers"]

help_message = discord.Embed(title="L'aide de zeubi", description="vraiment joli ce truc")
help_message.add_field(name="Commandes :", value="\n>spam <quantité> <mot>\n>test\n>invite\n")
help_message.set_footer(text="et puis voilà hein faut pas trop en demander non plus")

permissions_error = discord.Embed(title="Erreur !", description="", color=0xFC0303)
permissions_error.add_field(name="T'as pas les perms", value="Erreur de permissions, tu ne peut pas éxecuter cette commande")
permissions_error.set_footer(text="cheh mdr")

client = discord.Client()

def load_assets() :
    global ping_response
    with open('settings.json') as f:
        data = json.load(f)
    with open(responses, encoding="utf8") as fresp :
        ping_response = fresp.read().splitlines()

def perms_check(user_id) -> bool:
    if user_id in superusers :
        return (True)
    else :
        return (False)

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
        txt = ' '.join(message.content.split()[2:])
        try :
            n = int(message.content.split()[1])
        except (ValueError) :
            await message.channel.send("c'est pas comme ça que ça s'utilise <:1Head:814062704355704853>\nps : si tu demande gentiment je peux te donner de l'aide")
            return
        channel = client.get_channel(n)
        await channel.send(txt)
    elif message.content.startswith(">killbot") :
        if perms_check(message.author.mention) :
            await message.channel.send("c'est la fin de moi, ciao les gens")
            print(">killbot received, ending program")
            os._exit(0)
        else :
            await message.channel.send(embed=permissions_error)
            await message.channel.send("sal fou mdrr")

@client.event
async def on_ready():
    print(f"{client.user} est connecté à Discord !\nserveurs rejoints:")
    for guild in client.guilds:
        print(f"{guild.name} - id :{guild.id}")
    load_assets()

@client.event
async def on_message(message) :
    if bool(message.content) and message.content[0] == '>' :
        await commands_manager(message)
    elif "zeubi" in message.content and message.author != client.user :
        await message.channel.send("oué c'est moi")
    elif "coucou" in message.content and message.author != client.user :
        await message.channel.send("wesh wesh canne à pêche")
    elif "salut" in message.content and message.author != client.user :
        await message.channel.send("salut :)")
    elif "bash" in message.content and message.author != client.user :
        await man_bash(message)
    elif client.user.mentioned_in(message) :
        if (message.author.bot) :
            await message.channel.send("sale bot de merde")
        else :
            await message.channel.send(random.choice(ping_response))

client.run(TOKEN)