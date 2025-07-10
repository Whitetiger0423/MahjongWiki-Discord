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
        activity=discord.Game("!help"),
    )


# 응답 테스트
@bot.slash_command(name="핑")
async def Ping(ctx):
    embed = discord.Embed(
        title=f"PONG!", description="", color=EmbedColor["success"]
    )
    embed.add_field(name="", value="응답 완료!")
    await ctx.respond(embed=embed)



bot.run(os.getenv("BOT_TOKEN"))
