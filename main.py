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

idPlayer1 = ""
idPlayer2 = ""
turn = ""
gameOver = False
board = []
maxCard = 1
game = False

statusS = [[4, 1000, 100], [5, 1200, 150], [6, 1400, 200], [7, 1600, 250], [8, 1800, 300], [9, 2000, 350], [10, 2500, 500]]

def isAdmin(input:str):
    cursor.execute("SELECT * FROM player WHERE Admin = True AND ID_Dis = '%s' " %input)
    for row in cursor.fetchall():
        return True
    return False

@client.command()
async def hello(ctx):
    print("Hello")
    await ctx.send("บอทก็เห็นด้วย")

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
async def showBattle(ctx):
    idDis = str(idPlayer1)
    print(idDis)
    cursor.execute("SELECT * FROM cardPlayer where ID_Dis = '%s' AND Battle = True" % idDis)
    for row in cursor.fetchall():
        card = row.ID_Card
        url = ''
        cursor.execute("SELECT * FROM card where CardID = '%s'" % card)
        for col in cursor.fetchall():
            url = col.URL
        embed = discord.Embed(title=f"{'Battle List Player1 '}", description=('ข้อมูลสงครามของ <@' + idDis + '>'), color=discord.Color.red())
        embed.add_field(name='ID Card', value=f"{':id: ' + str(row.ID_Card)}")
        embed.add_field(name='HP', value=f"{':heart: ' + str(row.HP)}")
        embed.add_field(name='Attack', value=f"{':crossed_swords: ' + str(row.Att)}")
        # url = row.URL
        # print(url)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    idDis = str(idPlayer2)
    print(idDis)
    cursor.execute("SELECT * FROM cardPlayer where ID_Dis = '%s' AND Battle = True" % idDis)
    for row in cursor.fetchall():
        card = row.ID_Card
        url = ''
        cursor.execute("SELECT * FROM card where CardID = '%s'" % card)
        for col in cursor.fetchall():
            url = col.URL
        embed = discord.Embed(title=f"{'Battle List Player2 '}", description=('ข้อมูลสงครามของ <@' + idDis + '>'),
                              color=discord.Color.red())
        embed.add_field(name='ID Card', value=f"{':id: ' + str(row.ID_Card)}")
        embed.add_field(name='HP', value=f"{':heart: ' + str(row.HP)}")
        embed.add_field(name='Attack', value=f"{':crossed_swords: ' + str(row.Att)}")
        # url = row.URL
        # print(url)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@client.command()
async def choose(ctx):
    global turn
    global game
    global board
    idDis = str(ctx.author.id)
    print(idDis)
    print(turn)
    print(gameOver)
    if gameOver == True:
        print('not start')
    elif maxCard == 0:
        print('ยังไม่ได้เซ็ทจำนวนการ์ด')
    elif idDis == turn:
        game = True
        board = [":busts_in_silhouette:", ":vs:", ":robot:",
        ":white_large_square:", ":black_large_square:", ":white_large_square:"]

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]
        await ctx.send("เป๋ายิงฉุบเพื่อโจมตี rock–paper–scissors \n"
                       "เลือกค้อนพิมพ์ -att r \n"
                       "เลือกกรรไกรพิมพ์ -att s \n"
                       "เลือกกระดาษพิมพ์ -att p")
    else:
        await ctx.send("ไม่ใช่ตาของคุณ")
        print('no')

@client.command()
async def att(ctx, choice:str):
    global board
    markBot = ' '
    mark = ' '
    mylist = ["rock", "paper", "scissors"]
    my = random.choice(mylist)
    print(my)
    await ctx.send("บอทเลือก " + my)
    if my == 'rock':
        markBot = ':punch:'
    elif my == 'paper':
        markBot = ':hand_splayed:'
    else:
        markBot = ':v:'
    idDis = str(ctx.author.id)
    if game == True and turn == idDis and gameOver == False:
        if choice == 'r':
            mark = ':punch:'
        elif choice == 'p':
            mark = ':hand_splayed:'
        elif choice == 's':
            mark = ':v:'

        board[3] = mark
        board[5] = markBot

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

@client.command()
async def hp(ctx, damage: int):
    global turn
    global gameOver
    idDis = str(ctx.author.id)
    target = ''
    if gameOver == True:
        print("Game over already")
    elif idDis == turn:
        if idDis == idPlayer1:
            target = idPlayer2
            hp = 999999
            cursor.execute("SELECT * FROM cardPlayer where ID_Dis = '%s' AND Battle = True" % str(target))
            for row in cursor.fetchall():
                hp = row.HP
            hp = hp - damage
            if hp <= 0:
                print("End Game")
                cursor.execute("UPDATE cardPlayer SET HP = %d WHERE ID_DIS = '%s' " % (hp, str(target)))
                conn.commit()
                gameOver = True
            else:
                cursor.execute("UPDATE cardPlayer SET HP = %d WHERE ID_DIS = '%s' " % (hp, str(target)))
                conn.commit()
                turn = target
        elif idDis == idPlayer2:
            target = idPlayer1
            hp = 999999
            cursor.execute("SELECT * FROM cardPlayer where ID_Dis = '%s' AND Battle = True" % str(target))
            for row in cursor.fetchall():
                hp = row.HP
            hp = hp - damage
            if hp <= 0:
                print("End Game")
                cursor.execute("UPDATE cardPlayer SET HP = %d WHERE ID_DIS = '%s' " % (hp, str(target)))
                conn.commit()
                gameOver = True
            else:
                cursor.execute("UPDATE cardPlayer SET HP = %d WHERE ID_DIS = '%s' " % (hp, str(target)))
                conn.commit()
                turn = target
        else:
            print("มีบ้างอย่างผิดพลาด")

        cursor.execute("SELECT * FROM cardPlayer where ID_Dis = '%s' AND Battle = True" % target)
        for row in cursor.fetchall():
            card = row.ID_Card
            url = ''
            cursor.execute("SELECT * FROM card where CardID = '%s'" % card)
            for col in cursor.fetchall():
                url = col.URL
            embed = discord.Embed(title=f"{'Battle Report '}", description=('ข้อมูลสงครามของ <@' + target + '>'),
                                  color=discord.Color.red())
            embed.add_field(name='ID Card', value=f"{':id: ' + str(row.ID_Card)}")
            embed.add_field(name='HP', value=f"{':heart: ' + str(row.HP)}")
            embed.add_field(name='Attack', value=f"{':crossed_swords: ' + str(row.Att)}")
            # url = row.URL
            # print(url)
            embed.set_image(url=url)
            await ctx.send(embed=embed)
    else:
        print("ไม่ใช่ตาของคุณ")

@client.command()
async def arena(ctx, player1: discord.Member, player2: discord.Member):
    global idPlayer1
    global idPlayer2
    global turn
    global gameOver
    global game

    if gameOver == False:
        idPlayer1 = str(player1.id)
        idPlayer2 = str(player2.id)
        turn = ""
        game = False
        soul1 = 0
        soul2 = 0
        hp1 = 0
        hp2 = 0
        cursor.execute("SELECT * FROM cardPlayer where ID_Dis = '%s' AND Battle = True" % idPlayer1)
        for row in cursor.fetchall():
            card = row.ID_Card
            url = ''
            cursor.execute("SELECT * FROM card where CardID = '%s'" % card)
            for col in cursor.fetchall():
                url = col.URL
                soul1 = col.Soul
                print(soul1)
                i = 0
            while i < len(statusS):
                if soul1 == statusS[i][0]:
                    hp1 = statusS[i][1]
                    print(hp1)
                i += 1
            embed = discord.Embed(title=f"{'Battle List Player1 '}", description=('ข้อมูลสงครามของ <@' + idPlayer1 + '>'),
                                  color=discord.Color.red())
            embed.add_field(name='ID Card', value=f"{':id: ' + str(row.ID_Card)}")
            embed.add_field(name='HP', value=f"{':heart: ' + str(hp1)}")
            embed.add_field(name='Attack', value=f"{':crossed_swords: ' + str(row.Att)}")
            # url = row.URL
            # print(url)
            embed.set_image(url=url)
            await ctx.send(embed=embed)

        cursor.execute("SELECT * FROM cardPlayer where ID_Dis = '%s' AND Battle = True" % idPlayer2)
        for row in cursor.fetchall():
            card = row.ID_Card
            url = ''
            cursor.execute("SELECT * FROM card where CardID = '%s'" % card)
            for col in cursor.fetchall():
                url = col.URL
                soul2 = col.Soul
                print(soul1)
                i = 0
            while i < len(statusS):
                if soul2 == statusS[i][0]:
                    hp2 = statusS[i][1]
                    print(hp2)
                i += 1
            embed = discord.Embed(title=f"{'Battle List Player1 '}", description=('ข้อมูลสงครามของ <@' + idPlayer1 + '>'),
                                  color=discord.Color.red())
            embed.add_field(name='ID Card', value=f"{':id: ' + str(row.ID_Card)}")
            embed.add_field(name='HP', value=f"{':heart: ' + str(hp2)}")
            embed.add_field(name='Attack', value=f"{':crossed_swords: ' + str(row.Att)}")
            # url = row.URL
            # print(url)
            embed.set_image(url=url)
            await ctx.send(embed=embed)

        cursor.execute("UPDATE cardPlayer SET HP = %d WHERE ID_DIS = '%s' " % (hp1, str(idPlayer1)))
        conn.commit()
        cursor.execute("UPDATE cardPlayer SET HP = %d WHERE ID_DIS = '%s' " % (hp2, str(idPlayer2)))
        conn.commit()
        await ctx.send("----- Welcome to YOKEiPTO Land -----\n"
                    "------------ System ready ------------\n"
                    "Player1 is <@" + idPlayer1 + "> is ready!!! \n"
                    "Player2 is <@" + idPlayer2 + "> is ready!!!")

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = str(player1.id)
            await ctx.send("It is <@" + idPlayer1 + ">'s turn.")
        elif num == 2:
            turn = str(player2.id)
            await ctx.send("It is <@" + idPlayer2 + ">'s turn.")
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
    statusAdmin = isAdmin(str(ctx.author.id))
    print(statusAdmin)
    if statusAdmin == True:
        tmpData = False
        st = str(player.id)
        cursor.execute("SELECT * FROM cardPlayer WHERE ID_Card = '%s'" %dataIn1)
        for row in cursor.fetchall():
            tmpData = True

        print(st)
        print(dataIn1)
        hp = 0
        att = 0
        soul = 0
        cursor.execute("SELECT * FROM card WHERE CardID = '%s'" % dataIn1)
        for row in cursor.fetchall():
            soul = row.Soul
            print(soul)
        i = 0
        while i < len(statusS):
            if soul == statusS[i][0]:
                hp = statusS[i][1]
                att = statusS[i][2]
                print(hp)
                print(att)
            i+=1

        if tmpData == False:
            cursor.execute("INSERT INTO cardPlayer (ID_Dis, ID_Card, HP, Att) VALUES('%s', '%s', %d, %d)" %(st, dataIn1, hp, att))
            conn.commit()
            await ctx.send("add already")
            print("add already")
        else:
            cursor.execute("UPDATE cardPlayer SET ID_Dis = '%s', HP = %d, Att = %d WHERE ID_Card = '%s'" % (st, hp, att, dataIn1))
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
async def add(ctx, input:str):
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
            await ctx.send('การ์ดของคุณถูกเพิ่มไปแล้ว')
        else:
            num += 1
            print(input)

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

            hp = 0
            att = 0
            cursor.execute("SELECT * FROM card WHERE CardID = '%s'" % input)
            for row in cursor.fetchall():
                soul = row.Soul
                print(soul)
            i = 0
            while i < len(statusS):
                if soul == statusS[i][0]:
                    hp = statusS[i][1]
                    att = statusS[i][2]
                    print(hp)
                    print(att)
                i += 1

            cursor.execute("UPDATE cardPlayer SET Battle = True, Num_Battle = %d, HP = %d, Att = %d WHERE ID_Card = '%s'" % (num, hp, att, input))
            conn.commit()
            print('Update Already')
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