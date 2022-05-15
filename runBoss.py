import pyodbc
import discord
from discord.ext import commands
from config import *
import os
from datetime import datetime
import random

directory = os.getcwd()
directory = directory + '\DB.accdb'
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %directory)
cursor = conn.cursor()

# cursor.execute("INSERT INTO PlayerData (NameDis) VALUES('test')")
# conn.commit()
# print('Data Inserted')

# cursor.execute("SELECT COUNT(*) FROM PlayerUnit WHERE ID_Player = 0")
# fixture_count = cursor.fetchone()[0]
# # for row in cursor.fetchall():
# print(fixture_count)
#
#     cursor.execute("SELECT Name, HP FROM Unit WHERE Unit_ID = 'A2' ")
#
#     for row in cursor.fetchall():
#         if row.Name == 'Slave Host':
#             print(row.Name, row.HP)

client = commands.Bot(command_prefix="-")

@client.command()
async def info(ctx):
    await ctx.send("----- Welcome to Red Land Battle ----- \n"
                   "ℒ𝒶-𝒱𝑜𝒸𝓀 ℳ𝒶𝓂𝓂𝓊𝓉𝒽𝓊𝓈 ℒ𝑜𝓇𝒹 \n"
                   "La-vock คือ ช้างแมมมอธ ถึก ใหญ่ ยาว\n"
                   "เป็นงานcustomสวยๆ จากGrekkaครับ โดนได้รับจากการที่ถืองานในพันธมิตรเดียวกัน(ดูสีพื้นหลัง)\n"
                   "ครบ 14ตัว โดยจะแจกตอนนี้พันธมิตรละ 5ตัวเท่านั้น \n"
                   "และกิจกรรมในวันที่24 - 30 เมษานี้เป็นกิจกรรมโจมตี La-vock และลูกสมุน \n"
                   "โดยลูกสมุนจะออกมาปั่นป่วนผู้กล้าทุกท่าน5วัน โดยวันที่6กองที่จะเหลือรอดจะออกมาต้านผู้กล้าไว้ ก่อนจะพบกับบอสสุดโหด ถึกทน ยาวนาน \n")
    await ctx.send("-------------------------------------")

@client.command()
async def setP(ctx, player: discord.Member):
    # For Real
    # cursor.execute("SELECT * FROM Player")
    # for Test
    cursor.execute("SELECT * FROM Player")

    tmp = False
    nameDis = str(player)
    for row in cursor.fetchall():
        # print(type(nameDis))
        # print(type(row.NameDis))
        # print(tmp)
        if nameDis == row.NameDis:
            print(nameDis + " in list already")
            tmp = True
            break
    if tmp == False:
        # For Real
        # cursor.execute("INSERT INTO Player (NameDis) VALUES('%s')"%nameDis)
        # for Test
        cursor.execute("INSERT INTO Player (NameDis) VALUES('%s')"%nameDis)
        conn.commit()
        await ctx.send("ผู้เล่น/Player <@" + nameDis + "> ลงทะเบียนเรียบร้อยแล้ว / registered successfully")
        print('Data Inserted' + nameDis)
    else:
        await ctx.send("ผู้เล่น/Player <@" + nameDis + "> ลงทะเบียนไปแล้ว / already registered")

@client.command()
async def showUnit(ctx):
    cursor.execute("SELECT * FROM Unit ORDER BY Unit_ID")
    embed = discord.Embed(title=f"{'----------<Unit>----------'}", description=('แสดงเลขไอดีตัวUnit'),color=discord.Color.blue())
    for row in cursor.fetchall():
        embed.add_field(name=row.Unit_ID ,value=f"{'Name= '+ str(row.Name)}")
                # embed.set_thumbnail(url=f"{ctx.guild.icon}")
                # url = row.URL
                # print(url)
                # embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def showPlayer(ctx):
    nameUser = str(ctx.author)
    cursor.execute("SELECT Player.NameDis, PlayerUnit.ID_Unit, PlayerUnit.ID_Player, PlayerUnit.status, PlayerUnit.Num,"
                   "Unit.Name, Unit.Unit_ID FROM ((PlayerUnit  "
                   "INNER JOIN Player ON PlayerUnit.ID_Player = Player.ID)"
                   "INNER JOIN Unit ON PlayerUnit.ID_Unit = Unit.ID)")

    embed = discord.Embed(title=f"{'----------<Battle list of '+nameUser+'>----------'}", description=('แสดงUnit ที่เข้าแข่ง'),color=discord.Color.red())
    for row in cursor.fetchall():
        if nameUser == str(row[0]):
            status = ''
            if row[3] == False:
                status = 'พร้อมใช้งาน'
            else:
                status = 'ไม่พร้อมใช้งาน'
            embed.add_field(name='กองที่'+ str(row[4]), value=f"{str(row[6]) + ' | '+ str(row[5]) + ' | '+ status}")
                # embed.set_thumbnail(url=f"{ctx.guild.icon}")
                # url = row.URL
                # print(url)
                # embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def add(ctx, inputUnit:str):
    #Player
    cursor.execute("SELECT * FROM Player")
    tmpP = False
    nameP = ''
    idP = 0
    for row in cursor.fetchall():
        if str(ctx.author) == row.NameDis:
            print(row.NameDis + " Can add data")
            nameP = row.NameDis
            idP = row.ID
            tmpP = True
            break

    #Unit
    tmpU = False
    nameU = ''
    idU = 0

    cursor.execute("SELECT * FROM Unit WHERE Unit_ID = '%s'" %inputUnit)
    for row in cursor.fetchall():
            print(str(ctx.author) + ' can add '+row.Name)
            nameU = row.Name
            idU = row.ID
            tmpU = True
            break

    if tmpP == False:
        await ctx.send("<@" + str(ctx.author) + "> คุณยังไม่ได้ลงทะเบียน")
    elif tmpU == False:
        await ctx.send(inputUnit + " ไม่มีในรายการ")
    else:
        cursor.execute("SELECT COUNT(*) FROM PlayerUnit WHERE ID_Player = %d" % idP)
        fixture_count = cursor.fetchone()[0]
        print(fixture_count)
        if fixture_count >= 4:
            print("<@" + str(ctx.author) + "> Unit is limit")
            await ctx.send("<@" + str(ctx.author) + "> Unit ของคุณครบกำหนดแล้ว")
        else:
            cursor.execute("INSERT INTO PlayerUnit (ID_Unit, ID_Player, Num) VALUES('%d', '%d', '%d' )" % (idU, idP, (fixture_count+1)))
            conn.commit()
            await ctx.send('ผู้เล่น <@' + nameP + '> เพิ่ม ' + nameU)
            print('Data Inserted ' + nameP + ' ' + nameU)

@client.command()
async def showBoss(ctx):
    cursor.execute("SELECT * FROM Boss")
    for row in cursor.fetchall():
        embed = discord.Embed(title=f"{str(row.Name)}", description=('Unit ID: '+row.Unit_ID), color=discord.Color.blue())
        embed.add_field(name="เลือด", value=f"{int(row.HP)}")
        embed.add_field(name="จำนวน", value=f"{int(row.N)}")
        embed.add_field(name="เลือดรวม", value=f"{(int(row.N)*int(row.HP))}")
        embed.add_field(name="เพิ่มเกราะบอส", value=f"{(int(row.DF))}")
        embed.add_field(name="ลดWS ผู้เล่น", value=f"{(int(row.WS))}")
        # embed.set_thumbnail(url=f"{ctx.guild.icon}")
        url = row.URL
        # print(url)
        embed.set_image(url=url)

        await ctx.send(embed=embed)

@client.command()
async def sBoss(ctx, num: int):
    cursor.execute("SELECT * FROM Boss where ID = %d" %num)
    for row in cursor.fetchall():
        embed = discord.Embed(title=f"{str(row.Name)}", description=('Unit ID: '+row.Unit_ID), color=discord.Color.blue())
        embed.add_field(name="เลือด", value=f"{int(row.HP)}")
        embed.add_field(name="จำนวน", value=f"{int(row.N)}")
        embed.add_field(name="เลือดรวม", value=f"{(int(row.N)*int(row.HP))}")
        embed.add_field(name="เพิ่มเกราะบอส", value=f"{(int(row.DF))}")
        embed.add_field(name="ลดWS ผู้เล่น", value=f"{(int(row.WS))}")
        # embed.set_thumbnail(url=f"{ctx.guild.icon}")
        url = row.URL
        # print(url)
        embed.set_image(url=url)

        await ctx.send(embed=embed)

@client.command()
async def att(ctx, unit:int):

    #Player
    cursor.execute("SELECT * FROM Player")
    tmpP = False
    nameP = ''
    idP = 0
    for row in cursor.fetchall():
        if str(ctx.author) == row.NameDis:
            print(row.NameDis + " Can add data")
            nameP = row.NameDis
            idP = row.ID
            tmpP = True
            break

    #Unit
    tmpU = False
    id = 0
    idU = 0
    n = 0
    at = 0
    status = False

    cursor.execute("SELECT * FROM PlayerUnit WHERE Num = %d AND ID_Player = %d" %(unit, idP) )
    for row in cursor.fetchall():
            print(str(ctx.author) + ' can use '+str(row.ID))
            id = row.ID
            idU = row.ID_Unit
            status = row.status
            tmpU = True
            break
    print(idU)
    cursor.execute("SELECT * FROM Unit WHERE ID = %d" %idU)
    for row in cursor.fetchall():
        n = row.N
        at = row.AT
        url = str(row.URL)
        urlStatus = str(row.URL_Status)

    if tmpP == False:
        await ctx.send("<@" + str(ctx.author) + "> คุณยังไม่ได้ลงทะเบียน")
    elif tmpU == False:
        await ctx.send(str(unit) + " ไม่มีในรายการ")
    elif status == True:
        await ctx.send(str(unit) + " ใช้ตีไปแล้ว")
    else:
        # cursor.execute("INSERT INTO PlayerUnit (status) VALUES(True)")
        cursor.execute("UPDATE PlayerUnit SET status = True WHERE ID = %d" %id)
        conn.commit()
        sum = at*n
        await ctx.send("Unit ของคุณมี " + str(n) + "ตัว AT= " + str(at) + "\n" 
                       "ทอยลูกตามจำนวนด้านล่าง")
        await ctx.send("/roll notation: " + str(sum) + "d6s")
        await ctx.send(url)
        await ctx.send(urlStatus)
        print('Data Update ' + nameP + ' status ')

@client.command()
async def hp(ctx, unit:str, dmg:int):

    # Player
    cursor.execute("SELECT * FROM Player")
    tmpP = False
    nameP = ''
    idP = 0
    for row in cursor.fetchall():
        if str(ctx.author) == row.NameDis:
            print(row.NameDis + " Can add data")
            nameP = row.NameDis
            idP = row.ID
            tmpP = True
            break

    #date
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    # Assuming you have a cursor named cursor you want to execute this query on:
    cursor.execute("insert into History(ID_Player, DMG, HDate) values('%d', '%d', '%s')" %(idP, dmg, formatted_date))

    # Boss
    hp = 0
    n = 0
    idB = 0
    nameB = ''
    tmpB = False
    url = ''
    cursor.execute("SELECT * FROM WarBoss WHERE Unit_ID = '%s'" %unit)
    for row in cursor.fetchall():
        hp = row.HP
        n = row.N
        idB = row.ID
        tmpB = True
        nameB = row.Name
        url = row.URL
        print('Boss was attack ' + unit)

    hpBack = 0
    nBack = 0
    cursor.execute("SELECT * FROM Boss WHERE Unit_ID = '%s'" % unit)
    for row in cursor.fetchall():
        hpBack = row.HP
        nBack = row.N

    if tmpP == False:
        await ctx.send("<@" + str(ctx.author) + "> คุณยังไม่ได้ลงทะเบียน")
    elif tmpB == False:
        await ctx.send('ไม่มีในBoss ' + unit + ' ในรายการ')
    else:
        allHp = (hpBack * (n-1)) +hp
        print(allHp)
        calHp = allHp - dmg
        print(calHp)
        hpCal = 0
        nCal = 0
        if calHp <= 0 :
            await ctx.send(str(ctx.author) + ' โจมตี' + nameB + ", " + nameB + 'ได้กลับบ้านเกิดเรียบร้อย')
            cursor.execute("UPDATE WarBoss SET HP = 0, N = 0 WHERE Unit_ID = '%s' " % unit)
            conn.commit()
            embed = discord.Embed(title=f"{'-----<War Report>-----'}",
                                  description=(str(ctx.author) + ' โจมตี ' + nameB),
                                  color=discord.Color.red())
            embed.add_field(name="ผู้ทำดาเมจ", value=f"{str(ctx.author)}")
            embed.add_field(name="ดาเมจที่ทำได้", value=f"{int(dmg)}")
            embed.add_field(name="หมายเลข", value=f"{nameB}")
            embed.add_field(name="สถานะ", value=f"{'กลับบ้านเกิด ไปฟ้องแม่เรียบร้อย'}")
            # embed.set_thumbnail(url=f"{ctx.guild.icon}")
            # print(url)
            embed.set_image(url=url)

            await ctx.send(embed=embed)
        else:
            hpCal = int(calHp % hpBack)
            if hpCal == 0:
                nCal = (int(calHp / hpBack))
                hpCal = hpBack
            else:
                nCal = (int(calHp / hpBack))+1
            print(nCal)
            print(hpCal)
            await ctx.send(str(ctx.author) + ' โจมตี' + nameB + ", " + nameB + ' เหลือN: ' + str(nCal) + ' Hp: ' + str(hpCal) + ' รวมHp: ' + str(((nCal-1)*hpBack)+hpCal))
            cursor.execute("UPDATE WarBoss SET HP = %d, N = %d WHERE Unit_ID = '%s' " % (hpCal, nCal, unit))
            conn.commit()

            embed = discord.Embed(title=f"{'-----<War Report>-----'}",
                                  description=(str(ctx.author) + ' โจมตี ' + nameB),
                                  color=discord.Color.red())
            embed.add_field(name="ผู้ทำดาเมจ", value=f"{str(ctx.author)}")
            embed.add_field(name="ดาเมจที่ทำได้", value=f"{int(dmg)}")
            embed.add_field(name="หมายเลข", value=f"{nameB}")
            embed.add_field(name="เลือด", value=f"{int(hpCal)}")
            embed.add_field(name="จำนวนที่เหลือ", value=f"{int(nCal)}")
            embed.add_field(name="รวมเลือดที่เหลือ", value=f"{int(((nCal-1)*hpBack)+hpCal)}")
            # embed.set_thumbnail(url=f"{ctx.guild.icon}")
            # print(url)
            embed.set_image(url=url)

            await ctx.send(embed=embed)

            await ctx.send('-sWar ' + str(idB))

@client.command()
async def showWar(ctx):

    cursor.execute("SELECT * FROM WarBoss")
    for row in cursor.fetchall():
        realHP = 0
        cursor.execute("SELECT * FROM Boss where ID = %d" % row.ID)
        for row1 in cursor.fetchall():
            realHP = row1.HP
        embed = discord.Embed(title=f"{str(row.Name) + ' <War Status>'}", description=('Unit ID: '+row.Unit_ID), color=discord.Color.blue())
        embed.add_field(name="เลือด", value=f"{int(row.HP)}")
        embed.add_field(name="จำนวน", value=f"{int(row.N)}")
        embed.add_field(name="เลือดรวม", value=f"{((int(row.N)-1)*int(realHP))+int(row.HP)}")
        embed.add_field(name="เพิ่มเกราะบอส", value=f"{(int(row.DF))}")
        embed.add_field(name="ลดWS ผู้เล่น", value=f"{(int(row.WS))}")
        # embed.set_thumbnail(url=f"{ctx.guild.icon}")
        url = row.URL
        # print(url)
        embed.set_image(url=url)

        await ctx.send(embed=embed)

@client.command()
async def sWar(ctx, num: int):
    realHP = 0
    cursor.execute("SELECT * FROM Boss where ID = %d" % num)
    for row in cursor.fetchall():
        realHP = row.HP
    cursor.execute("SELECT * FROM WarBoss where ID = %d" %num)alert
    for row in cursor.fetchall():
        embed = discord.Embed(title=f"{str(row.Name) + ' <War Status>'}", description=('Unit ID: '+row.Unit_ID), color=discord.Color.blue())
        embed.add_field(name="เลือด", value=f"{int(row.HP)}")
        embed.add_field(name="จำนวน", value=f"{int(row.N)}")
        embed.add_field(name="เลือดรวม", value=f"{((int(row.N)-1)*int(realHP))+int(row.HP)}")
        embed.add_field(name="เพิ่มเกราะบอส", value=f"{(int(row.DF))}")
        embed.add_field(name="ลดWS ผู้เล่น", value=f"{(int(row.WS))}")
        # embed.set_thumbnail(url=f"{ctx.guild.icon}")
        url = row.URL
        # print(url)
        embed.set_image(url=url)

        await ctx.send(embed=embed)

@client.command()
async def calDmg(ctx):

    cursor.execute("SELECT * FROM Player")
    for row in cursor.fetchall():
        id = row.ID
        dmg = 0
        count = 0
        avg = 0.0
        cursor.execute("SELECT * FROM History WHERE ID_Player = %d" %id)
        for row1 in cursor.fetchall():
            dmg += row1.DMG
            count += 1
        print(dmg)
        print(count)
        if count == 0:
            cursor.execute("UPDATE Player SET DMG = %d, Count = %d, Average = %.2f WHERE ID = %d" % (dmg, count, avg, id))
            conn.commit()
        else:
            avg = (1.0*dmg)/count
            print(avg)
            cursor.execute("UPDATE Player SET DMG = %d, Count = %d, Average = %f WHERE ID = %d" % (dmg, count, avg, id))
            conn.commit()

@client.command()
async def score(ctx):
    cursor.execute('SELECT * FROM Player')
    embed = discord.Embed(title=f"{'----------<Score Board>----------'}", description=('กระดานแสดงค่าแต่ละคน'),color=discord.Color.blue())
    for row in cursor.fetchall():
        if(row.DMG > 0):
            embed.add_field(name=row.NameDis, value=f"{'DMG= ' + str(row.DMG)}")
            # embed.set_thumbnail(url=f"{ctx.guild.icon}")
            # url = row.URL
            # print(url)
            # embed.set_image(url=url)

    await ctx.send(embed=embed)

@client.command()
async def buff(ctx):
    bu = ["ลดdmg -1 ให้ตัวหลัก ถ้าdmg=1 ให้Att -1",
          "เพิ่มAtt +1 ให้ท่าโจมตีหลัก(ท่าแรก)",
          "เพิ่มst +1 ให้ตัวหลัก",
          "ลดws -1 ให้ตัวหลัก",
          "เพิ่มAtt +2 ให้ท่าโจมตีหลัก(ท่าแรก)",
          "เพิ่มws +1 ให้ตัวหลัก",
          "ลดws -1 ให้ตัวหลัก",
          "เพิ่มAtt +3ให้ท่าโจมตีหลัก(ท่าแรก)",
          "เพิ่มst +1 ให้ตัวหลัก",
          "เพิ่มAtt X2 ให้ท่าโจมตีหลัก(ท่าแรก)",
          "ลดws -1 ให้ตัวหลัก",
          "เพิ่มN +1 ให้ตัวหลัก(ไม่นับลูกน้องหรือตัวขี่)",
          "ลดst -1 ให้ตัวหลัก",
          "เพิ่มN +2 ให้ตัวหลัก(ไม่นับลูกน้องหรือตัวขี่)",
          "เพิ่มws +1 ให้ตัวหลัก",
          "เพิ่มdmg +1 ให้ตัวหลัก(ไม่นับลูกน้องหรือตัวขี่)",
          "เพิ่มst +1 ให้ตัวหลัก",
          "เพิ่มdmg +1 ให้ตัวลูกน้องหรือตัวขี(ไม่นับตัวหลัก)",
          "ลดdmg -1 ให้ตัวหลัก ถ้าdmg=1 ให้Att -1",
          "เพิ่มatt +1 ให้ตัวลูกน้องหรือตัวขี่(ไม่นับตัวหลัก)",
          "เพิ่มws +1 ให้ตัวหลัก",
          "ลดst -1 ให้ตัวหลัก",
          "เพิ่มatt +2 ให้ตัวลูกน้องหรือตัวขี่(ไม่นับตัวหลัก)",
          "เพิ่มst +1 ให้ตัวหลัก",
          "ได้โอกาสใช้ท่าหลักตีบอสเพิ่ม 1 ครั้ง",
          "ได้โอกาสใช้ลูกน้องหรือสัตว์ขี่ตีบอสเพิ่ม 1 ครั้ง",
          "เพิ่มws +1 ให้ตัวหลัก",
          "เพิ่มst +1 ให้ตัวหลัก",
          "ลดN -1 ให้ตัวหลัก ถ้าN=1 ให้Att -1"]

    n = random.randrange((len(bu)*8))
    print(n)
    n = n % len(bu)
    print(n)
    embed = discord.Embed(title=f"{'----------<Random buffs>----------'}", description=('กระดานเสี่ยงโชค'),color=discord.Color.blue())
    embed.add_field(name=':sos:', value=f"{bu[n]}")
    await ctx.send(embed=embed)

@client.command()
async def set(ctx, num: int, unit: str):
    nameUser = str(ctx.author)
    unit_id = 0
    unit_name = ''
    user_id = 0
    cursor.execute("SELECT * FROM Unit")
    for row in cursor.fetchall():
        if unit == str(row.Unit_ID):
            unit_id = row.ID
            unit_name = row.Name
            tmp = True

    cursor.execute("SELECT * FROM Player")
    for row in cursor.fetchall():
        if nameUser == str(row.NameDis):
            user_id = row.ID

    if user_id == 0:
        await ctx.send("<@" + str(ctx.author) + "> คุณยังไม่ได้ลงทะเบียน")
    elif unit_id == 0:
        await ctx.send("<@" + str(unit) + "> ไม่พบยูนิตนี้")
    elif num != 1 and num != 2 and num != 3 and num != 4:
        await ctx.send("<@" + str(num) + "> ไม่พบกองนี้")
    else:
        cursor.execute("UPDATE PlayerUnit SET ID_Unit = %d WHERE Num = %d AND ID_Player = %d" % (unit_id, num, user_id))
        conn.commit()
        await ctx.send("<" + str(unit_name) + "> ลงทะเบียน ตำแหน่ง->" + str(num) +  " เรียบร้อย")




client.run(TOKEN, bot=True, reconnect=True)