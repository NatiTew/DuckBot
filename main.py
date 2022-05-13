from builtins import print
import discord
from discord.ext import commands
from config import *
import pyodbc
import os
import random

directory = os.getcwd()
directory = directory + '\DB.accdb'
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %directory)
cursor = conn.cursor()

client = commands.Bot(command_prefix="-")

player1 = ""
player2 = ""
turn = ""
gameOver = True
board = []

statusS = [[4, 1000, 100], [5, 1200, 150], [6, 1400, 200], [7, 1600, 250], [8, 1800, 300], [9, 2000, 350], [10, 2500, 500]]

@client.command()
async def hello(ctx):
    print("Hello")
    await ctx.send("World!")


@client.command()
async def show(ctx, input:str):
    cursor.execute("SELECT * FROM card where CardID = '%s'" %input)
    idCard = ''
    name = ''
    soul = 0
    rarity = ''
    URL = ''
    info = ''

    hp = 0
    att = 0

    for row in cursor.fetchall():
        idCard = row.CardID
        print(idCard)
        name = row.Name
        print(name)
        soul = row.Soul
        rarity = row.Rarity
        URL = row.URL
        info = row.info

    i = 0
    while i < len(statusS):
        if (statusS[i][0] == soul):
            hp = statusS[i][1]
            print(statusS[i][1])
            att = statusS[i][2]
            print(statusS[i][2])
        i += 1

    embed = discord.Embed(title=f"{str(name)}", description=(str(info)),color=discord.Color.blue())
    embed.add_field(name='ID Card' ,value=f"{':id: '+str(idCard)}")
    embed.add_field(name='Soul', value=f"{':ghost: '+str(soul)}")
    embed.add_field(name='Rarity', value=f"{str(rarity)}")
    embed.add_field(name='HP', value=f"{':heart: '+str(hp)}")
    embed.add_field(name='Attack', value=f"{':crossed_swords: '+str(att)}")
    embed.set_thumbnail(url=f"{'https://cdn.discordapp.com/attachments/972124143325679676/974184935525064754/YK_ARENA.JPG'}")
    # url = row.URL
    # print(url)
    embed.set_image(url=URL)
    await ctx.send(embed=embed)

@client.command()
async def showAll(ctx, input:str):
    cursor.execute("SELECT * FROM card")
    idCard = ''
    name = ''

    embed = discord.Embed(title=f"{str(name)}", description=(str(info)), color=discord.Color.blue())
    for row in cursor.fetchall():
        idCard = row.CardID
        print(idCard)
        name = row.Name
        print(name)
        embed.add_field(name='ID Card' ,value=f"{':id: '+str(idCard)}")

    await ctx.send(embed=embed)


@client.command()
async def arena(ctx, player1: discord.Member, player2: discord.Member):
    print(player1)
    print(player1.id)
    global idPlayer1
    global idPlayer2
    global turn
    global gameOver

    if gameOver:
        # global board
        # board = [":busts_in_silhouette:", ":vs:", ":robot:",
        # ":white_large_square:", ":black_large_square:", ":white_large_square:"]

        idPlayer1 = str(player1.id)
        idPlayer2 = str(player2.id)
        turn = ""
        gameOver = False

        await ctx.send("----- Welcome to YOKEiPTO Land -----\n"
                    "------------ System ready ------------")

        await ctx.send("Player1 is <@" + idPlayer1 + "> is ready!!! \n"
                       "Player2 is <@" + idPlayer2 + "> is ready!!!")

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + idPlayer1 + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + idPlayer2 + ">'s turn.")

        # print the board
        # line = ""
        # for x in range(len(board)):
        #     if x == 2 or x == 5 or x == 8:
        #         line += " " + board[x]
        #         await ctx.send(line)
        #         line = ""
        #     else:
        #         line += " " + board[x]
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one."
                       "ขณะนี้เกมส์กำลังเริ่มอยู่ โปรดรอให้เกมส์จบก่อน")

@client.command()
async def setAdmin(ctx, player: discord.Member):
    nameDis = ' '
    cursor.execute("SELECT * FROM player WHERE NameDis = '%s'" % player)
    for row in cursor.fetchall():
        nameDis = row.NameDis

    if nameDis == ' ':
        cursor.execute("INSERT INTO player (NameDis, ID_DIS, Admin) VALUES('%s', '%s', True )" % (player, player.id))
        conn.commit()
    else:
        cursor.execute("UPDATE player SET Admin = True WHERE ID_DIS = '%s' " % str(player.id))
        conn.commit()

    if int(ctx.author.id) == AEP_ID:
        await ctx.send("Set Admin already \n"
                       "ลงทะเบียนแอดมินเรียบร้อย")
    else:
        await ctx.send("You can't set Admin \n"
                       "คุณไม่สามารถใช้คำสั่งนี้ได้")

@client.command()
async def getAdmin(ctx):
    cursor.execute("SELECT NameDis FROM player WHERE Admin = True")
    for row in cursor.fetchall():
        await ctx.send(row.NameDis)

@client.command()
async def setCard(ctx):
    cursor.execute("SELECT NameDis FROM player WHERE Admin = True")
    for row in cursor.fetchall():
        await ctx.send(row.NameDis)

@client.command()
async def getmsg(ctx, msgID: int):
    msg = await ctx.fetch_message(msgID)

@arena.error
async def arena_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.\n"
                       "-arena <tag player1> <tag player2>")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

client.run(TOKEN, bot=True, reconnect=True)