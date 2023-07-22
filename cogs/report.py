import disnake
from disnake.ext import commands
import datetime

import time
import sqlite3

db = sqlite3.connect("server.db") 
cur = db.cursor()

class Button(disnake.ui.View):
    def __init__(self,member):
        super().__init__(timeout=None)
        self.member = member

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green)
    async def confirm(self,button: disnake.ui.Button,inter: disnake.MessageInteraction):
        await self.member.send(embed = disnake.Embed(
                    title = "Ваш репорт был принят",
                    description = f"Ваша репорт был принят на расмотрение модератором - {inter.author.mention}\n",
                    ).set_thumbnail(
            url = self.member.avatar)
        )
        # await self.client.send_message(self.member, "Your message goes here")
        self.value = True
        self.stop()
        await inter.message.delete()
        if cur.execute(f"SELECT id FROM users WHERE id = ?", [inter.author.id]).fetchone() is None:
            cur.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", [inter.author.id, 0, 0, 0, 0, 0, 0, 0, 0])
            db.commit()
        else:
            
            cur.execute("UPDATE users SET points = points + 5 WHERE id = {}".format(inter.author.id))
            cur.execute("UPDATE users SET reports = reports + 1 WHERE id = {}".format(inter.author.id))
            db.commit()
    
    @disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.red)
    async def decline(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.member.send(embed = disnake.Embed(
                    title = "Ваша заявка была отклонена",
                    description = f"{self.member.mention} Ваша репорт был отклонён модератором - {inter.author.mention}\n",
                    ).set_thumbnail(
            url = self.member.avatar)
        )
        self.value = True
        self.stop()
        await inter.message.delete();
        
class Reports(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.member = None
        print('Commands {} is loaded'.format(self.__class__.__name__))
    
    @commands.slash_command(name='report', description='Снятие стафф ролей')

    async def report(self, inter, target: disnake.Member = commands.Param(name = "пользователь"),message: str = commands.Param(name = "причина")):
        channel = self.client.get_channel(1132346310566084628)
        self.member = inter.author
        if target == inter.author:
            embed = disnake.Embed(
                title = "Взаимодействие с участником",
                description = "Вы не можете взаимодействовать с самим собой"
            ).set_author(
                name = target,
                url = f"https://discordapp.com/users/{target.id}/",
                icon_url = target.avatar
            ).set_thumbnail(
                url = target.avatar
            )
            await inter.send(embed = embed, ephemeral = True)
            return True
        else:
            embed = disnake.Embed(
                    description = f"Репорт на {target.mention} был успешно отправлен",
                    color = 0x2f3136)
            
            await channel.send(
                    embed = disnake.Embed(
                title = "Жалоба",
                description = "Пользователь оставил жалобу"
            ).set_author(
                name = target,
                url = f"https://discordapp.com/users/{target.id}/",
                icon_url = target.avatar
            ).set_thumbnail(
                url = target.avatar
            ).add_field(    
                    name = "Отправитель:",
                    value = f"{inter.author.mention}/`{inter.author.id}`",
                    inline = False
            ).add_field(
                    name = "Пользователь:",
                    value = f"{target.mention}/`{target.id}`",
                    inline = False
            ).add_field(    
                    name = "Причина:",
                    value = f"{message} ",
                    inline = False
            )
            )
            await inter.send(embed = embed,ephemeral = True)
            await channel.send(view=Button(self.member))
            
def setup(client):
    client.add_cog(Reports(client))