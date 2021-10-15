#!/usr/bin/python
#coding=utf8

import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

ping_response = open('ping_response.txt', encoding="utf8").read().splitlines()

help_message = discord.Embed(title="L'aide de zeubi", description="vraiment joli ce truc")
help_message.add_field(name="Commandes :", value="\n>spam <quantité> <mot>\n>test\n>invite\n")
help_message.set_footer(text="et puis voilà hein faut pas trop en demander non plus")

client = discord.Client()

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
    while (i < qty) :
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
    if ">test" in message.content and message.author != client.user :
        await message.channel.send("tester c'est douter")
    elif ">spam" in message.content and message.author != client.user :
        await spam(message)
    elif ">help" in message.content and message.author != client.user  :
        help_message.set_thumbnail(url=message.guild.icon_url)
        await message.channel.send(embed=help_message)
    elif ">invite" in message.content and message.author != client.user  :
        await message.channel.send("voilà le lien d'invitation espèce de bg : https://discord.com/api/oauth2/authorize?client_id=890884345018069032&permissions=8&scope=bot")

@client.event
async def on_ready():
    print(f"{client.user} est connecté à Discord !\nserveurs rejoints:")
    for guild in client.guilds:
        print(f"{guild.name} - id :{guild.id}")

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