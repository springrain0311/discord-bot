import discord
import gspread
import asyncio
import os
from flask import Flask
from threading import Thread
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import tasks
import datetime

# =========================
# 🔐 환경 변수
# =========================
import os

TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

print("TOKEN:", TOKEN)
print("CHANNEL_ID:", CHANNEL_ID)

CHANNEL_ID = int(CHANNEL_ID)
# =========================
# 🌐 웹서버 (Render 유지용)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

# =========================
# 📊 구글 시트 연결
# =========================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join(os.getcwd(), "service_account.json"), scope
)
gc = gspread.authorize(creds)

# =========================
# 🤖 디스코드 설정
# =========================
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# =========================
# 📤 랭킹 전송
# =========================
async def send_ranking():
    sheet = gc.open("봄비길드 수로랭킹").sheet1
    data = sheet.get_all_values()

    ranking_text = ""

    for i in range(1, min(21, len(data))):
        rank = int(data[i][0])
        name = data[i][1]
        score = data[i][2]

        if rank == 1:
            icon = "🥇"
        elif rank == 2:
            icon = "🥈"
        elif rank == 3:
            icon = "🥉"
        elif 4 <= rank <= 10:
            icon = "🌸"
        else:
            icon = "✨"

        ranking_text += f"{icon} {rank}위 {name} │ {score}\n"

    embed = discord.Embed(
        title="🌸 봄비길드 수로 랭킹 TOP20 🌸",
        description=ranking_text,
        color=0xff99cc
    )

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
    else:
        print("채널 못찾음")

# =========================
# ⏰ 매주 목요일 00:00 실행
# =========================
@tasks.loop(minutes=1)
async def scheduler():
    now = datetime.datetime.now()

    if now.weekday() == 3 and now.hour == 0 and now.minute == 0:
        print("랭킹 전송 실행")
        await send_ranking()

# =========================
# 🚀 시작
# =========================
@client.event
async def on_ready():
    print(f"로그인됨: {client.user}")
    scheduler.start()

client.run(TOKEN)