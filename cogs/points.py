import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
import sqlite3

connection = sqlite3.connect("server.db") 
cursor = connection.cursor()

from pymongo import MongoClient

#code for db MongoDB

cluster = MongoClient('')
db = cluster["Yakumi"]
collection = db["Users"]

class Back(disnake.ui.View):

    def __init__(self, author, target):
        self.author = author
        self.target = target
        super().__init__(timeout=None)

    async def interaction_check(self, interaction):
        if interaction.user == self.author or interaction.user == self.author:
            return True
        else:
            return False

    @disnake.ui.button(label="Назад", style=ButtonStyle.red)
    async def Back(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        reports = cursor.execute("SELECT reports FROM users WHERE id = {}".format(self.target.id)).fetchone()[0]            
        rebuke = cursor.execute("SELECT rebuke FROM users WHERE id = {}".format(self.target.id)).fetchone()[0]            
        points = cursor.execute("SELECT points FROM users WHERE id = {}".format(self.target.id)).fetchone()[0]
        verefy = cursor.execute("SELECT verefy FROM users WHERE id = {}".format(self.target.id)).fetchone()[0]
        vetifBan = cursor.execute("SELECT vetifBan FROM users WHERE id = {}".format(self.target.id)).fetchone()[0]
        mutes = cursor.execute("SELECT mutes FROM users WHERE id = {}".format(self.target.id)).fetchone()[0]
        bans = cursor.execute("SELECT bans FROM users WHERE id = {}".format(self.target.id)).fetchone()[0]
        warns = cursor.execute("SELECT warns FROM users WHERE id = {}".format(self.target.id)).fetchone()[0]

        user = collection.find_one({
            "user_id" : f"{self.target.id}"
            
            })

        userstr = str(user)
        userstr = userstr.replace("\'", "\"")
        userstr = userstr.split(',')

        isin = False
        for i in range(len(userstr)):
            strrr = userstr[i]
            if strrr[2] == 'v':
                bal_str = userstr[i].split(": ")
                isin = True
                    
        if isin == True:        
                coins = int(bal_str[1].replace("}", ""))
                # coins /= 1000
                # coins /= 60
                # coins /= 60
                coins_min= (coins % 3600000) / 60000
                roundedcoins=round(coins_min, 1)
                coins = f"{coins // 3600000} ч. {roundedcoins} мин."  
                
        embed = disnake.Embed(
                title = f"Профиль staff — {self.target}",
                description= ""
            ).set_thumbnail(
                url = self.target.avatar
            )
        embed.add_field(
            name='> Принято репортов',
            value=f'```{reports}```',
            inline=True
            )
        embed.add_field(
            name='> Выдано верефов',
            value=f'```{verefy}```',
            inline=True
            )
        embed.add_field(
            name='> Выдано недопусков',
            value=f'```{vetifBan}```',
            inline=True
            )
            
        embed.add_field(
            name='> Выдано мутов',
            value=f'```{mutes}```',
            inline=True
            )
        embed.add_field(
            name='> Выдано Банов',
            value=f'```{bans}```',
            inline=True
            )
        embed.add_field(
            name='> Выдано варнов',
            value=f'```{warns}```',
            inline=True
            )
        embed.add_field(
            name='> Голосовая активность',
            value=f'```{coins}```',
            inline=False
            )
        embed.add_field(
            name='> Выговоры',
            value=f'```{rebuke}```',
            inline=True
            )
        embed.add_field(
            name='> Баллы',
            value=f'```{points}```',
            inline=False
            )
        
        await interaction.response.edit_message(embed=embed, view = Top(self.author, self.target))

class Top(disnake.ui.View):

    def __init__(self, author, target):
        self.author = author
        self.target = target
        super().__init__(timeout=None)

    async def interaction_check(self, interaction):
        if interaction.user == self.author or interaction.user == self.author:
            return True
        else:
            await interaction.response.send_message(embed = disnake.Embed(
            description = "Вы не можете использовать кнопку другого пользователя"
        ), ephemeral = True)
            return False
    
    @disnake.ui.button(label="Топ очков", style=ButtonStyle.primary)
    async def TopPoint(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):

        counter = 0
        embed = disnake.Embed(title='ТОП-10 членов стаффа по очкам', color=0x2f3136)
        embed.set_thumbnail(url=interaction.author.display_avatar)
        members = []
        for row in cursor.execute("SELECT id, points FROM users ORDER BY points DESC LIMIT 10"):
            member = disnake.utils.get(interaction.guild.members, id=row[0])
            counter += 1
            
            members.append(f'**{counter}** {member.mention} — {int(round(row[1]))} очков')
        i = f"\n".join(members)
        embed.add_field(
            name=f'Пользователи',
            value = f"{i}",
            inline = False
        )
        await interaction.response.edit_message(embed=embed, view=Back(self.author, self.target))

class Staff_profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Commands {} is loaded'.format(self.__class__.__name__))

    @commands.slash_command(name='staff-profile', description='Показать профиль стафф')
    async def support(self, inter, target: disnake.Member = commands.Param(name="пользователь")):

        if cursor.execute("SELECT id FROM users WHERE id = {}".format(target.id)).fetchone() == None:
            embed = disnake.Embed(
                title = "Профиль саппорта",
                description = "У данного юзера, нет стафф профиля"
            ).set_thumbnail(
                url = target.avatar
            )
            await inter.send(embed = embed, ephemeral=True)
        else:
            reports = cursor.execute("SELECT reports FROM users WHERE id = {}".format(target.id)).fetchone()[0]            
            rebuke = cursor.execute("SELECT rebuke FROM users WHERE id = {}".format(target.id)).fetchone()[0]            
            points = cursor.execute("SELECT points FROM users WHERE id = {}".format(target.id)).fetchone()[0]
            verefy = cursor.execute("SELECT verefy FROM users WHERE id = {}".format(target.id)).fetchone()[0]
            vetifBan = cursor.execute("SELECT vetifBan FROM users WHERE id = {}".format(target.id)).fetchone()[0]
            mutes = cursor.execute("SELECT mutes FROM users WHERE id = {}".format(target.id)).fetchone()[0]
            bans = cursor.execute("SELECT bans FROM users WHERE id = {}".format(target.id)).fetchone()[0]
            warns = cursor.execute("SELECT warns FROM users WHERE id = {}".format(target.id)).fetchone()[0]

            user = collection.find_one({
            "user_id" : f"{target.id}"
            
            })

            userstr = str(user)
            userstr = userstr.replace("\'", "\"")
            userstr = userstr.split(',')

            isin = False
            for i in range(len(userstr)):
                strrr = userstr[i]
                if strrr[2] == 'v':
                    bal_str = userstr[i].split(": ")
                    isin = True
                    
            if isin == True:        
                coins = int(bal_str[1].replace("}", ""))
                # coins /= 1000
                # coins /= 60
                # coins /= 60
                coins_min= (coins % 3600000) / 60000
                roundedcoins=round(coins_min, 1)
                coins = f"{coins // 3600000} ч. {roundedcoins} мин."  
                
            embed = disnake.Embed(
                title = f"Профиль staff — {target}",
                description= ""
            ).set_thumbnail(
                url = target.avatar
            )
            embed.add_field(
            name='> Принято репортов',
            value=f'```{reports}```',
            inline=True
            )
            embed.add_field(
            name='> Выдано верефов',
            value=f'```{verefy}```',
            inline=True
            )
            embed.add_field(
            name='> Выдано недопусков',
            value=f'```{vetifBan}```',
            inline=True
            )
            
            embed.add_field(
            name='> Выдано мутов',
            value=f'```{mutes}```',
            inline=True
            )
            embed.add_field(
            name='> Выдано Банов',
            value=f'```{bans}```',
            inline=True
            )
            embed.add_field(
            name='> Выдано варнов',
            value=f'```{warns}```',
            inline=True
            )
            embed.add_field(
            name='> Голосовая активность',
            value=f'```{coins}```',
            inline=False
            )
            embed.add_field(
            name='> Выговоры',
            value=f'```{rebuke}```',
            inline=True
            )
            embed.add_field(
            name='> Баллы',
            value=f'```{points}```',
            inline=False
            )

            await inter.send(embed = embed, view = Top(inter.author, target))

    @support.error
    async def on_command_error(self, inter, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = disnake.Embed(
                title="Недостаточно прав!",
                description=f"{inter.author.mention} у вас нет прав на это действие!"
            )
            await inter.send(embed=embed, ephemeral=True)

            

def setup(client):
    client.add_cog(Staff_profile(client))