import discord
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

# =========================
# 환경변수
# =========================
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# =========================
# 구글 시트 인증
# =========================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account.json", scope
)
gc = gspread.authorize(creds)

# =========================
# 디스코드 봇 설정
# =========================
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# =========================
# 랭킹 전송 함수
# =========================
async def send_ranking():
    sheet = gc.open("봄비길드 수로랭킹").sheet1
    data = sheet.get_all_values()

    ranking_text = ""

    for i in range(1, 21):
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
    await channel.send(embed=embed)

# =========================
# 봇 시작 시 실행
# =========================
@client.event
async def on_ready():
    print(f"로그인됨: {client.user}")

    await send_ranking()

# =========================
# 실행
# =========================
client.run(TOKEN)