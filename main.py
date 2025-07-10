import discord
import os
import dotenv
import logging
import utils.logging
from discord.ext import commands, tasks
import time
from asyncio import sleep


# .env 불러오기 / 로깅 세팅
dotenv.load_dotenv()
utils.logging.setup_logging()

# Discord Intents 활성화
intents = discord.Intents.default()
intents.message_content = True

# 접두어 설정 / 로깅 시작
bot = discord.Bot(intents=intents)
# discord.Intents.all()
logger = logging.getLogger("main")

# 엠베드 색 지정
EmbedColor = {"default": 0xDADADA, "success": 0x77DADA, "error": 0xB32424}

# slash command group 지정
debate = bot.create_group("토론", "토론 포스트를 생성하는 명령어입니다.")

# 시작 시간 기록
bot.start_time = time.time()

# 준비
@bot.event
async def on_ready():
    guild_count = len(bot.guilds)
    # 가동 시작
    logger.info(f"Logged in as {bot.user.name}")
    logger.info(f"Be used in {guild_count} guilds.")
    # 활동 변경
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("V 0.0.0 (alpha)"),
    )


# 응답 테스트
@bot.slash_command(name="핑")
async def Ping(ctx):
    embed = discord.Embed(
        title=f"PONG!", description="", color=EmbedColor["success"]
    )
    embed.add_field(name="", value="응답 완료!")
    await ctx.respond(embed=embed)


@debate.command(name="보통문서", description=("보통문서에 관한 토론 포스트를 생성합니다."))
async def Normal(ctx, article: discord.Option(str, name="문서명", description="토론 대상이 되는 문서 이름을 작성해주세요."), reason: discord.Option(str, name="발제이유", description="발제하는 이유를 5글자 안팎으로 간단하게 요약해서 적어주세요.")):
    wikiGuild = bot.get_guild(1392679550730637382)
    try:
        guildUser = await wikiGuild.fetch_member(ctx.author.id)
    except discord.NotFound:
        await ctx.respond("마작위키 서버에 참여하셔야 명령어를 사용할 수 있습니다.", ephemeral=True)
        return
    print(guildUser.roles) #debug
    if 1392684765068394698 in guildUser.roles:
        normalForum = bot.get_channel(1392690787447214130)
        newThread = await normalForum.create_thread(
        name=f"{article} - {reason}",
        content=f"발제자: <@{ctx.user.id}>"
        )
        await ctx.respond(f"{newThread.jump_url} 토론이 생성되었습니다!")
        await newThread.starting_message.edit(content=f"발제자: <@{ctx.user.id}>\n문서의 최상단 분류 아래에 `[include (틀:디스코드 토론,url={newThread.jump_url})]`을 삽입해주세요.")
    else:
        await ctx.respond("마작위키 계정이 인증되지 않았습니다. <#1392679551825346633>에서 인증을 진행해주시고, 이미 인증 요청을 했다면 잠시 기다려주세요.", ephemeral=True)


bot.run(os.getenv("BOT_TOKEN"))
