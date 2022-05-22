from builtins import print
import discord
from discord.ext import commands
from config import *
import pyodbc
import os
import random
from datetime import datetime

directory = os.getcwd()
directory = directory + '\DB_Bid.accdb'
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %directory)
cursor = conn.cursor()

client = commands.Bot(command_prefix="+")

bidStatus = False
max = 2.5
h = 22
m = 25
s = 0
addTime = "22:30:00"
dis_id_odd = ''

num = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]

def check(input:int):
    i = 0
    while i<len(num):
        if i == input:
            return num[i]
        i += 1
    return str(input)

@client.command()
async def bid(ctx, input:float):
    global bidStatus
    global max
    global h
    global m
    global s
    global addTime
    global dis_id_odd
    idDis = ctx.author.id
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    endTime = check(h)+":"+check(m)+":"+check(s)
    formatted_time = now.strftime('%H:%M:%S')
    formatted_H = now.strftime('%H')
    formatted_M = now.strftime('%M')
    formatted_S = now.strftime('%S')
    intH = int(formatted_H)
    intM = int(formatted_M)
    intS = int(formatted_S)

    if formatted_time < endTime:
        print(bidStatus)
        print(formatted_date)
        print(str(ctx.author.id))
        id = str(ctx.author.id)
        print(max)
        if bidStatus == False:
            await ctx.send('<@' + str(ctx.author.id) + '>การประมูลยังไม่ได้เริ่ม หรือสิ้นสุดแล้ว')
        elif input > max:
            embed = discord.Embed(title=f"{' <Alert Auction>'}",
                                  description=('@everyone สมาชิก <@' + str(idDis) + '> ได้ทำการประมูล'),
                                  color=discord.Color.dark_red())
            embed.add_field(name="เวลา", value=f"{formatted_date}")
            embed.add_field(name="ชื่อ", value=f"{'<@' + str(idDis) + '>'}")
            embed.add_field(name="ราคาประมูล", value=f"{'%.2f Near'}" % input)
            embed.add_field(name="หมดเวลาประมูล", value=f"{'%s น. GMT+7'}" %endTime)
            embed.add_field(name="ผู้ประมูลก่อนหน้า", value=f"{'<@%s>'}" % str(dis_id_odd))
            await ctx.send(embed=embed)

            await ctx.send("สมาชิก/Member <@" + str(dis_id_odd) + "> มีคนประมูลราคาสูงกว่าคุณ คุณมีเวลาประมูลในราคาที่สูงกว่าก่อนเวลา " + str(endTime) + "น.(เพิ่มเติมเมื่อหมดเวลา จะนับถอยหลัง5นาที ไม่มีคนสู้ถือเป็นที่สุดค่ะ)")
            max = input
            dis_id_odd = idDis
        elif input < max:
            await ctx.send(
                "สมาชิก/Member <@" + id + "> คุณลงราคาต่ำกว่าราคาขั้นต่ำในการบิด  / Price Below the minimum bid price.")
        else:
            await ctx.send("Error โปรดลงราคาใหม่")
    elif formatted_time >= endTime:
        print(formatted_time)
        print(addTime)
        if formatted_time < addTime:
            await ctx.send("ช่วงต่อเวลา")
            chIntM = intM + 5
            if chIntM >=60:
                intH += 1
                chIntM = chIntM%60
            addTime = check(intH) + ":" + check(chIntM) + ":" + check(intS)
            if bidStatus == False:
                await ctx.send('<@' + str(ctx.author.id) + '>การประมูลยังไม่ได้เริ่ม หรือสิ้นสุดแล้ว')
            elif input > max:
                embed = discord.Embed(title=f"{' <Alert Auction>'}",
                                      description=('@everyone สมาชิก <@' + str(idDis) + '> ได้ทำการประมูล'),
                                      color=discord.Color.dark_red())
                embed.add_field(name="เวลา", value=f"{formatted_date}")
                embed.add_field(name="ชื่อ", value=f"{'<@' + str(idDis) + '>'}")
                embed.add_field(name="ราคาประมูล", value=f"{'%.2f Near'}" % input)
                embed.add_field(name="หมดเวลาประมูล", value=f"{'%s น. GMT+7'}" % addTime)
                embed.add_field(name="ผู้ประมูลก่อนหน้า", value=f"{'<@%s>'}" % str(dis_id_odd))
                await ctx.send(embed=embed)
                await ctx.send("สมาชิก/Member <@" + str(dis_id_odd) + "> มีคนประมูลราคาสูงกว่าคุณ คุณมีเวลาประมูลในราคาที่สูงกว่าก่อนเวลา " + str(addTime)+"น.")
                max = input
                dis_id_odd = idDis
            elif input < max:
                await ctx.send(
                    "สมาชิก/Member <@" + id + "> คุณลงราคาต่ำกว่าราคาขั้นต่ำในการบิด  / Price Below the minimum bid price.")
            else:
                await ctx.send("Error โปรดลงราคาใหม่")
            print(addTime)
        else:
            await ctx.send("หมดเวลาประมูลแล้วจ้า")
            bidStatus = False
            print(bidStatus)
            print(formatted_time)
    else:
        await ctx.send("error")

@client.command()
async def startBid(ctx):
    global bidStatus
    if int(ctx.author.id) == AEP_ID:
        bidStatus = True
        await ctx.send("เริ่มBid / Start Bid")
@client.command()
async def endBid(ctx):
    global bidStatus
    if int(ctx.author.id) == AEP_ID:
        bidStatus = False
        await ctx.send("สิ้นสุดBid / End Bid")


@client.command()
async def hello(ctx):
    await ctx.send('เผางานๆๆๆๆ <@952814969097957377>')

client.run(TOKEN, bot=True, reconnect=True)