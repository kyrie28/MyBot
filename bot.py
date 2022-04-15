import discord
from discord.ext import commands
import asyncio
import maplecrawler
import maplerefs

f = open("token.txt", "r", encoding="utf-8")
token = f.read()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


def print_msg_info(message):
    print(f"[{message.author}]\t{message.content}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def ping(ctx):
    print_msg_info(ctx.message)
    await ctx.send(f"pong! {round(round(bot.latency, 4)*1000)}ms")


@bot.command()
async def hello(ctx):
    print_msg_info(ctx.message)
    await ctx.send(f"Hello, {ctx.message.author.mention}!")


@bot.command()
async def count(ctx, num=5):
    print_msg_info(ctx.message)
    for i in range(num):
        await ctx.send(num - i)
        await asyncio.sleep(1)


@bot.command(name="메이플")
async def maple(ctx, CharName=None):
    if not CharName:
        await ctx.send("사용법: !메이플 <캐릭터 이름>")
        return

    CharInfo = maplecrawler.GetCharacterInfo(CharName)
    if not CharInfo:
        await ctx.send(
            embed=discord.Embed(description="존재하지 않는 캐릭터입니다.", color=0xFF9D00)
        )
        return

    CharInfoEmbed = discord.Embed(title=CharInfo["이름"], color=0xFF9D00)
    CharInfoEmbed.set_image(
        url=CharInfo["캐릭터 이미지"].replace("https://", "http://").replace("/180", "")
    )
    for key in maplerefs.display_keys:
        if key in CharInfo.keys():
            CharInfoEmbed.add_field(name=key, value=CharInfo[key], inline=True)
    await ctx.send(embed=CharInfoEmbed)


bot.run(token)
