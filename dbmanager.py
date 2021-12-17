#!/usr/bin/env python3
#coding=utf8

from os import truncate
import discord
from logger import writelog
import mysql.connector

def test_connection(sqlconfig: dict) :
    try :
        SQL = mysql.connector.connect(**sqlconfig)
        cursor = SQL.cursor()
        cursor.execute(f"SELECT DISTINCT * FROM discord_bot.server;")
        return True
    except Exception :
        return False

def update_servers(sqlconfig: dict, client: discord.Client) :
    SQL = mysql.connector.connect(**sqlconfig)
    cursor = SQL.cursor()
    writelog(title="SQL(server)", message="Updating server table in database...")
    cursor.execute(f"SELECT DISTINCT * FROM discord_bot.server;")
    result = cursor.fetchall()
    cursor.close()
    idx = 0
    for guild in client.guilds:
        for r in result :
            if int(r[0]) == int(guild.id) :
                del result[idx]
                break
            idx = idx + 1
    cursor = SQL.cursor()
    for re in result : #servers that are not accessible anymore (bot was banned, server closed, etc...)
        cursor.execute(f"DELETE FROM discord_bot.server WHERE server_id = {re[0]};")
        SQL.commit()
    for guild in client.guilds: #making sure that everyone is in the database again
        cursor.execute(f"SELECT * FROM discord_bot.server WHERE server_id = {guild.id} ;")
        result = cursor.fetchall()
        if not bool(result) :
            cursor.execute(f"INSERT INTO discord_bot.server VALUES ('{guild.id}',\"{guild.name}\", DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT);")
        SQL.commit()
    cursor.close()
    SQL.close()
    writelog(title="SQL(server)", message="Server update finished, database is ready and up-to-date")
    return

def update_member(sqlconfig: dict, member: discord.member = None) -> None :
    SQL = mysql.connector.connect(**sqlconfig)
    cursor = SQL.cursor()
    cursor.execute(f"SELECT distinct * FROM discord_bot.member WHERE member_id = {member.id};")
    result = cursor.fetchall()
    if not bool(result) :
        try :
            writelog(title="SQL(member)", message=f"Creating entry for {member.name} in table")
            cursor.execute(f"INSERT INTO discord_bot.member VALUES ('{member.id}','<@!{member.id}>', '{member.name}', 0, 0, 0);")
            SQL.commit()
        except Exception as ex:
            writelog(title="SQL(member)", message=f"Creating entry for {member.name} failed, {ex}")
            raise
    else :
        if member.name != result[0][2] :
            try :
                writelog(title="SQL(member)", message=f"{member.name} is not up to date with database, updating...")
                cursor.execute(f"UPDATE discord_bot.member SET member_id='{member.id}', tag = '<@!{member.id}>', display_name = '{member.name}', xp = 0, level = 0, money = 0 WHERE member_id = {member.id};")
                SQL.commit()
                writelog(title="SQL(member)", message=f"Update complete for {member.name}")
            except Exception as ex:
                writelog(title="SQL(member)", message=f"Updating entry for {member.name} failed, {ex}")
                raise
    cursor.close()
    SQL.close()
    return

def register_new_server(sqlconfig: dict, guild: discord.Guild) :
    writelog(title="SQL(server)", message="New server joined, updating database...")
    SQL = mysql.connector.connect(**sqlconfig)
    cursor = SQL.cursor()
    try :
        cursor.execute(f"INSERT INTO discord_bot.server VALUES ('{guild.id}',\"{guild.name}\", DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT);")
        SQL.commit()
        writelog(title="SQL(server)", message="Update complete")
        cursor.close()
        SQL.close()
    except Exception as ex :
        writelog(title="SQL(server)", message=f"Error while registering new server, ex : {ex}", error=True)
        cursor.close()
        SQL.close()
        raise

def remove_server(sqlconfig: dict, guild: discord.Guild) :
    writelog(title="SQL(server)", message="Client left a server, updating database...")
    SQL = mysql.connector.connect(**sqlconfig)
    cursor = SQL.cursor()
    try :
        cursor.execute(f"DELETE FROM discord_bot.server WHERE server_id = '{guild.id}';")
        SQL.commit()
        writelog(title="SQL(server)", message="Update complete")
        cursor.close()
        SQL.close()
    except Exception as ex :
        writelog(title="SQL(server)", message=f"Error while removing old server, ex : {ex}", error=True)
        cursor.close()
        SQL.close()
        raise

def get_member_count(sqlconfig: dict) -> int:
    SQL = mysql.connector.connect(**sqlconfig)
    cursor = SQL.cursor()
    writelog(title="SQL", message="Retrieving member count")
    try :
        cursor.execute("SELECT COUNT(distinct member_id) FROM discord_bot.member;")
        result = cursor.fetchone()
        count = int(result[0])
    except Exception as ex :
        writelog(title="SQL", message=f"Retrieving member count failed, ex : {ex}")
        raise
    writelog(title="SQL", message=f"Member count = {count}")
    return (count)

def get_server_count(sqlconfig: dict) -> int:
    SQL = mysql.connector.connect(**sqlconfig)
    cursor = SQL.cursor()
    writelog(title="SQL", message="Retrieving server count")
    cursor.execute("SELECT COUNT(distinct server_id) FROM discord_bot.server;")
    result = cursor.fetchone()
    count = int(result[0])
    writelog(title="SQL", message=f"Server count = {count}")
    return (count)

def add_reaction_role(sqlconfig: dict, role_id: str, message_id: str, channel_id: str, server_id: str) -> None :
    writelog(title="SQL(reaction roles)", message="New reaction roles requested, updating database...")
    SQL = mysql.connector.connect(**sqlconfig)
    cursor = SQL.cursor()
    try :
        cursor.execute(f"INSERT INTO discord_bot.reaction_roles (id_message, id_channel, id_server, id_role, reaction) VALUES ('{message_id}', '{channel_id}', '{server_id}', '{role_id}');")
        SQL.commit()
        writelog(title="SQL(reaction roles)", message="Update complete")
        cursor.close()
        SQL.close()
    except Exception as ex :
        writelog(title="SQL", message=f"Updating reaction roles failed, ex : {ex}")
        raise

def check_reaction_role(sqlconfig: dict, server: discord.Guild, message_id: str, emoji: str) -> discord.Role :
    SQL = mysql.connector.connect(**sqlconfig)
    cursor = SQL.cursor(buffered=True)
    try :
        cursor.execute(f"SELECT distinct id_role FROM discord_bot.reaction_roles WHERE id_message = '{message_id}' and reaction = '{emoji}';")
        SQL.commit()
        result = cursor.fetchone()
        try :
            role_id = result[0]
        except TypeError :
            cursor.close()
            SQL.close()
            return (None)
        cursor.close()
        SQL.close()
    except Exception as ex :
        writelog(title="SQL", message=f"Getting reaction roles from database failed, ex : {ex}")
        raise
    try :
        role = discord.utils.get(server.roles, id=int(role_id))
    except AttributeError as ex:
        writelog(title="UTILS.GET(reaction roles)", message=f"Fetching reaction roles failed, ex : {ex}")
        raise
    writelog(title="UTILS.GET(reaction roles)", message="Success, role found")
    return (role)