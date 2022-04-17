import discord
from discord.ext import commands
import asyncio
from maplecrawler import get_character_info
import maplerefs
from ydl import download_from_youtube

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


@bot.command()
async def echo(ctx, *user_input):
    output = "".join(str(s) + " " for s in user_input)[:-1]
    await ctx.send(f"{ctx.message.author.mention} {output}")


@bot.command(aliases=["메", "메이플", "메이플스토리"])
async def maple(ctx, char_name=None):
    if not char_name:
        await ctx.send(f"{ctx.message.author.mention} 사용법: !메이플 <캐릭터 이름>")
        return

    char_info = get_character_info(char_name)
    if not char_info:
        await ctx.send(
            embed=discord.Embed(description="존재하지 않는 캐릭터입니다.", color=0xFF9D00)
        )
        return

    char_info_embed = discord.Embed(title=char_info["이름"], color=0xFF9D00)
    char_info_embed.set_image(
        url=char_info["캐릭터 이미지"].replace("https://", "http://")  # .replace("/180", "")
    )
    for key in maplerefs.display_keys:
        if key in char_info.keys():
            char_info_embed.add_field(name=key, value=char_info[key], inline=True)
    await ctx.send(embed=char_info_embed)


async def connect_helper(ctx):
    if not ctx.author.voice:
        await ctx.send(f"{ctx.message.author.mention} 명령어를 사용하기 위해서는 음성 채널에 접속해야 합니다.")
        return True
    elif not ctx.voice_client:
        await ctx.send(f"{ctx.message.author.mention} 음성 채널에 연결 중...")
        await ctx.author.voice.channel.connect()
        return True
    elif not ctx.voice_client.channel == ctx.author.voice.channel:
        await ctx.voice_client.disconnect()
        await ctx.send(f"{ctx.message.author.mention} 음성 채널에 연결 중...")
        await ctx.author.voice.channel.connect()
        return True
    else:
        return False


@bot.command(aliases=["연결"])
async def connect(ctx):
    if not await connect_helper(ctx):
        await ctx.send(f"{ctx.message.author.mention} 이미 음성 채널에 연결되었습니다.")


@bot.command(aliases=["연결해제", "연결끊기", "leave", "나가기"])
async def disconnect(ctx):
    if ctx.voice_client:
        voice = ctx.voice_client
        await ctx.send(f"{ctx.message.author.mention} 음성 채널을 나갑니다.")
        await voice.disconnect()
    else:
        await ctx.send(f"{ctx.message.author.mention} 연결된 음성 채널이 없습니다.")


@bot.command(aliases=["재생"])
async def play(ctx, *user_input):
    if not user_input:
        # Argument가 없고, pause 상태일 경우 음악 재생을 재개함
        if ctx.voice_client and ctx.voice_client.is_paused():
            await ctx.send(f"{ctx.message.author.mention} 음악을 다시 재생합니다.")
            ctx.voice_client.resume()
        else:
            await ctx.send(
                f"{ctx.message.author.mention} 사용법: !재생 <YouTube URL 또는 키워드>"
            )
            return

    # 음성 채널에 연결
    await connect_helper(ctx)

    # 유튜브로부터 음악 다운로드
    URL = download_from_youtube(user_input)
    if not URL:
        await ctx.send(f"{ctx.message.author.mention} 올바르지 않은 YouTube URL 또는 키워드입니다.")
        return

    # 음악 재생
    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }
    if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
        ctx.voice_client.stop()
    await ctx.send(f"{ctx.message.author.mention} 음악 재생 준비 중...")
    ctx.voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))


@bot.command(aliases=["일시정지"])
async def pause(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            await ctx.send(f"{ctx.message.author.mention} 음악을 일시정지합니다.")
            ctx.voice_client.pause()
        else:
            await ctx.send(f"{ctx.message.author.mention} 재생 중인 음악이 없습니다.")
    else:
        await ctx.send(f"{ctx.message.author.mention} 연결된 음성 채널이 없습니다.")


@bot.command(aliases=["정지"])
async def stop(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            await ctx.send(f"{ctx.message.author.mention} 음악을 정지합니다.")
            ctx.voice_client.stop()
        else:
            await ctx.send(f"{ctx.message.author.mention} 재생 중인 음악이 없습니다.")
    else:
        await ctx.send(f"{ctx.message.author.mention} 연결된 음성 채널이 없습니다.")


bot.run(token)
