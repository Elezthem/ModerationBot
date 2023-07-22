import disnake
from disnake.ext import commands

import os

from config.table_create import tablecreate

import sqlite3

from config.settings import settings

connection = sqlite3.connect("server.db") 
cursor = connection.cursor()

client = commands.Bot(command_prefix = '!', intents=disnake.Intents.all(), test_guilds=[1128609972536750203])
client.remove_command('help')

tablecreate()

@client.command()
@commands.has_permissions(administrator=True)
async def nick(inter, member: disnake.Member, nickname):
    await member.edit(nick=nickname)

@client.event
async def on_ready():
    await client.change_presence(status=disnake.Status.online, activity= disnake.Game('/report - Жалоба'))
    print(f"{client.user.name} запущен(а)")

async def load_extension(): 
    for commands in settings['commands']:
        try:
            client.load_extension(commands)
        except Exception as e:
            print(f"Ошибка загрузки команд: {e}") 

    for errors in settings['errors']:
        try:
            client.load_extension(errors)
        except Exception as e:
            print(f"Ошибка загрузки ошибок: {e}") 
 
    for events in settings['events']:
        try:
            client.load_extension(events)
        except Exception as e:
            print(f"Ошибка загрузки событий: {e}")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    tablecreate()
    await load_extension()
    await client.start(settings["TOKEN"])


if __name__ == '__main__':
    client.loop.run_until_complete(main())
    