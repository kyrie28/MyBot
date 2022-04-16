import discord
from discord.ext import commands
import asyncio
from maplecrawler import GetCharacterInfo
import maplerefs
import youtube_dl

f = open("token.txt", "r", encoding="utf-8")
token = f.read()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")


@bot.command()
async def ping(ctx):
    await ctx.send(
        f"{ctx.message.author.mention} pong! {round(round(bot.latency, 4)*1000)}ms"
    )


@bot.command(aliases=["hi", "안녕", "안녕하세요"])
async def hello(ctx):
    await ctx.send(f"안녕하세요, {ctx.message.author.mention}!")


@bot.command(aliases=["메", "메이플", "메이플스토리"])
async def maple(ctx, charName=None):
    if not charName:
        await ctx.send(f"{ctx.message.author.mention} 사용법: !메이플 <캐릭터 이름>")
        return

    charInfo = GetCharacterInfo(charName)
    if not charInfo:
        await ctx.send(
            embed=discord.Embed(description="존재하지 않는 캐릭터입니다.", color=0xFF9D00)
        )
        return

    charInfoEmbed = discord.Embed(title=charInfo["이름"], color=0xFF9D00)
    charInfoEmbed.set_image(
        url=charInfo["캐릭터 이미지"].replace("https://", "http://")  # .replace("/180", "")
    )
    for key in maplerefs.display_keys:
        if key in charInfo.keys():
            charInfoEmbed.add_field(name=key, value=charInfo[key], inline=True)
    await ctx.send(embed=charInfoEmbed)


# 1개의 VoiceClient만 사용하는 음악 재생 기능
@bot.command(aliases=["재생"])
async def play(ctx, url=None):

    # 유저가 음성 채널에 접속해 있지 않을 경우
    if not ctx.author.voice:
        await ctx.send(f"{ctx.message.author.mention} 명령어를 사용하기 위해서는 음성 채널에 접속해야 합니다.")
        return

    # 봇이 음성 채널에 접속해 있지 않을 경우
    if bot.voice_clients == []:
        if not url:
            await ctx.send(f"{ctx.message.author.mention} 사용법: !재생 <YouTube URL>")
            return
        await ctx.author.voice.channel.connect()
        await ctx.send(
            f"{ctx.message.author.mention} [{str(bot.voice_clients[0].channel)}] 음성 채널에 연결 중..."
        )

    voice = bot.voice_clients[0]
    if not url:
        # Argument가 없고, pause 상태일 경우 음악 재생을 재개함
        if voice.is_paused():
            await ctx.send(f"{ctx.message.author.mention} 음악을 다시 재생합니다.")
            voice.resume()
        else:
            await ctx.send(f"{ctx.message.author.mention} 사용법: !재생 <YouTube URL>")
            return

    ydl_opts = {"format": "bestaudio"}
    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }

    # 유튜브로부터 음악 다운로드
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info["formats"][0]["url"]

    # 음악 재생
    await ctx.send(f"{ctx.message.author.mention} 음악 재생 중...")
    if voice.is_playing() or voice.is_paused():
        voice.stop()
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))


@bot.command(aliases=["disconnect", "나가기"])
async def leave(ctx):
    if bot.voice_clients:
        await ctx.send(
            f"{ctx.message.author.mention} [{str(bot.voice_clients[0].channel)}] 음성 채널을 나갑니다."
        )
        await bot.voice_clients[0].disconnect()
    else:
        await ctx.send(f"{ctx.message.author.mention} 연결된 음성 채널이 없습니다.")


@bot.command(aliases=["일시정지"])
async def pause(ctx):
    if bot.voice_clients:
        voice = bot.voice_clients[0]
        if voice.is_playing():
            await ctx.send(f"{ctx.message.author.mention} 음악을 일시정지합니다.")
            await voice.pause()
        else:
            await ctx.send(f"{ctx.message.author.mention} 재생 중인 음악이 없습니다.")
    else:
        await ctx.send(f"{ctx.message.author.mention} 연결된 음성 채널이 없습니다.")


@bot.command(aliases=["정지"])
async def stop(ctx):
    if bot.voice_clients:
        voice = bot.voice_clients[0]
        if voice.is_playing() or voice.is_paused():
            await ctx.send(f"{ctx.message.author.mention} 음악을 정지합니다.")
            await voice.stop()
        else:
            await ctx.send(f"{ctx.message.author.mention} 재생 중인 음악이 없습니다.")
    else:
        await ctx.send(f"{ctx.message.author.mention} 연결된 음성 채널이 없습니다.")


bot.run(token)
