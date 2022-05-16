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
maxCard = 4

statusS = [[4, 1000, 100], [5, 1200, 150], [6, 1400, 200], [7, 1600, 250], [8, 1800, 300], [9, 2000, 350], [10, 2500, 500]]

@client.command()
async def hello(ctx):
    print("Hello")
    await ctx.send("ดิสอะไรน่าเผาจัง")


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
async def showAll(ctx):
    cursor.execute("SELECT * FROM card")
    idCard = ''
    nameCard = ''
    count = 1
    for row in cursor.fetchall():
        if (count%25) == 1:
            embed = discord.Embed(title=f"{'Show All ID Cards'}", description=('แสดงข้อมูลID การ์ด'), color=discord.Color.blue())
        idCard = row.CardID
        print(idCard)
        nameCard = row.Name
        print(nameCard)
        embed.add_field(name=nameCard ,value=f"{':id: '+str(idCard)}")
        if (count%25) == 0:
            await ctx.send(embed=embed)
        count += 1

@client.command()
async def arena(ctx, player1: discord.Member, player2: discord.Member):
    global idPlayer1
    global idPlayer2
    global turn
    global gameOver

    if gameOver == False:
        # global board
        # board = [":busts_in_silhouette:", ":vs:", ":robot:",
        # ":white_large_square:", ":black_large_square:", ":white_large_square:"]

        idPlayer1 = str(player1.id)
        idPlayer2 = str(player2.id)
        turn = ""
        gameOver = True

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
    if int(ctx.author.id) == AEP_ID:
        await ctx.send("Set Admin already \n"
                       "ลงทะเบียนแอดมินเรียบร้อย")
        nameDis = ' '
        cursor.execute("SELECT * FROM player WHERE NameDis = '%s'" % player)
        for row in cursor.fetchall():
            nameDis = row.NameDis

        if nameDis == ' ':
            cursor.execute(
                "INSERT INTO player (NameDis, ID_DIS, Admin) VALUES('%s', '%s', True )" % (player, player.id))
            conn.commit()
        else:
            cursor.execute("UPDATE player SET Admin = True WHERE ID_DIS = '%s' " % str(player.id))
            conn.commit()
    else:
        await ctx.send("You can't set Admin \n"
                       "คุณไม่สามารถใช้คำสั่งนี้ได้")

@client.command()
async def getAdmin(ctx):
    cursor.execute("SELECT NameDis FROM player WHERE Admin = True")
    for row in cursor.fetchall():
        await ctx.send(row.NameDis)

@client.command()
async def setCard(ctx, player: discord.Member, dataIn:str):
    dataIn1 = dataIn.upper()
    print(input)
    cursor.execute("SELECT ID_Dis FROM player WHERE Admin = True")
    statusAdmin = False
    for row in cursor.fetchall():
        if row.ID_Dis == str(ctx.author.id):
            statusAdmin = True

    print(statusAdmin)
    if statusAdmin == True:
        tmpData = False
        st = str(player.id)
        cursor.execute("SELECT * FROM cardPlayer WHERE ID_Card = '%s'" %dataIn1)
        for row in cursor.fetchall():
            print(row)
            tmpData = True

        print(st)
        print(dataIn1)
        if tmpData == False:
            cursor.execute("INSERT INTO cardPlayer (ID_Dis, ID_Card) VALUES('%s', '%s')" %(st, dataIn1))
            conn.commit()
            await ctx.send("add already")
            print("add already")
        else:
            cursor.execute("UPDATE cardPlayer SET ID_Dis = '%s' WHERE ID_Card = '%s'" % (st, dataIn1))
            conn.commit()
            await ctx.send("update already")
            print("update already")
    else:
        print('You are not admin')

@client.command()
async def my(ctx):
    cursor.execute("SELECT * FROM cardPlayer WHERE ID_Dis = '%s'" %str(ctx.author.id))
    idCard = ''
    embed = discord.Embed(title=f"{'แสดงข้อมูลการ์ด'}", description=('แสดงข้อมูลการ์ดของ<@'+str(ctx.author.id)+'>'), color=discord.Color.blue())
    for row in cursor.fetchall():
        idCard = str(row.ID_Card)
        sBattle = ''
        if(row.Battle == True):
            sBattle = 'พร้อมใช้งาน'
        else:
            sBattle = 'ไม่พร้อมใช้งาน'
        print(idCard)
        embed.add_field(name=str(idCard), value=f"{'สถานะ: '+sBattle}")
    await ctx.send(embed=embed)

@client.command()
async def who(ctx, player: discord.Member):
    cursor.execute("SELECT * FROM cardPlayer WHERE ID_Dis = '%s'" %str(player.id))
    idCard = ''
    embed = discord.Embed(title=f"{'แสดงข้อมูลการ์ด'}", description=('แสดงข้อมูลการ์ดของ<@'+str(player.id)+'>'), color=discord.Color.blue())
    for row in cursor.fetchall():
        idCard = str(row.ID_Card)
        sBattle = ''
        if(row.Battle == True):
            sBattle = 'พร้อมใช้งาน'
        else:
            sBattle = 'ไม่พร้อมใช้งาน'
        print(idCard)
        embed.add_field(name=str(idCard), value=f"{'สถานะ: '+sBattle}")
    await ctx.send(embed=embed)

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

@client.command()
async def set(ctx, input:str):
    global maxCard
    idDis = ' '
    nameCard = ' '
    soul = 0
    rarity = ' '
    url = ' '
    battle = False
    cursor.execute("SELECT * FROM cardPlayer WHERE ID_Card = '%s'" %str(input))
    for row in cursor.fetchall():
        idDis = str(row.ID_Dis)
        print(idDis)
        battle = row.Battle
    print(ctx.author.id)
    print(idDis)
    dis_id = str(ctx.author.id)

    num = 0
    cursor.execute("SELECT * FROM cardPlayer WHERE ID_Dis = '%s' AND Battle = True" % str(dis_id))
    for row in cursor.fetchall():
        num += 1
    print(num)

    if(idDis == dis_id):
        if num > maxCard:
            await ctx.send('การ์ดของคุณครบ' + str(maxCard) + ' ใบแล้ว')
        elif battle == True:
            c
        else:
            num += 1
            print(input)
            cursor.execute("UPDATE cardPlayer SET Battle = True, Num_Battle = %d WHERE ID_Card = '%s'" % (num, input))
            conn.commit()
            print('Update Already')
            cursor.execute("SELECT * FROM card WHERE cardID = '%s'" % input)
            for row in cursor.fetchall():
                nameCard = str(row.Name)
                soul = row.Soul
                rarity = row.Rarity
                url = row.URL
            embed = discord.Embed(title=f"{'อัพเดตสถานะ'}",
                                  description=('อัพเดตข้อมูลการ์ดของ<@' + str(idDis) + '>'),
                                  color=discord.Color.dark_red())
            embed.add_field(name='ID Card', value=f"{str(input)}")
            embed.add_field(name='Name Card', value=f"{str(nameCard)}")
            embed.add_field(name='Soul', value=f"{str(soul)}")
            embed.add_field(name='Rarity', value=f"{str(rarity)}")
            embed.add_field(name='Status', value=f"{'พร้อมใช้งาน'}")
            embed.set_image(url=url)
            await ctx.send(embed=embed)
    else:
        print('Can not Update')
        await ctx.send("Can not Update")

@client.command()
async def playMode(ctx, input:int):
    global maxCard
    global gameOver
    maxCard = input
    print(maxCard)
    gameOver = False
    await ctx.send('กำหนดจำนวนการ์ดที่ลงเรียบร้อย')
    cursor.execute("UPDATE cardPlayer SET Battle = False, Num_Battle = 0")
    conn.commit()
    await ctx.send('ล้างค่าสถานะเรียบร้อย')




client.run(TOKEN, bot=True, reconnect=True)