import discord
import gspread
import os
import asyncio
import json
from oauth2client.service_account import ServiceAccountCredentials

# 🔐 환경변수
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# 🔐 구글 인증
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gc = gspread.authorize(creds)

# 디코 설정
intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def send_ranking():
    print("🚀 랭킹 전송 시작")

    sheet = gc.open("봄비길드 수로랭킹").sheet1
    data = sheet.get_all_values()

    print("📊 데이터 개수:", len(data))

    ranking_text = ""

    # 🏆 TOP 3
    ranking_text += "🏆 **TOP 3**\n"
    for i in range(1, 4):
        rank = int(data[i][0])
        name = data[i][1]
        score = int(data[i][2])

        icons = ["🥇", "🥈", "🥉"]
        icon = icons[i-1]

        ranking_text += f"{icon} **{rank}위** │ `{name}`\n　　└ 💖 **{score:,}**\n\n"

    ranking_text += "━━━━━━━━━━━━━━━━━━\n\n"

    # 🌸 4~10위
    for i in range(4, 11):
        rank = int(data[i][0])
        name = data[i][1]
        score = int(data[i][2])

        ranking_text += f"🌸 {rank:>2}위 │ `{name}` │ {score:,}\n"

    ranking_text += "\n"

    # ✨ 11~20위
    for i in range(11, 21):
        rank = int(data[i][0])
        name = data[i][1]
        score = int(data[i][2])

        ranking_text += f"✨ {rank:>2}위 │ `{name}` │ {score:,}\n"

    embed = discord.Embed(
        title="🌸 봄비길드 수로 랭킹 🌸",
        description=ranking_text,
        color=0xffb6c1
    )

    channel = client.get_channel(CHANNEL_ID)
    print("📢 채널 객체:", channel)

    if channel is None:
        print("❌ 채널 못찾음 (ID 확인)")
        return

    await channel.send(embed=embed)
    print("✅ 메시지 전송 완료")


@client.event
async def on_ready():
    print(f"✅ 로그인됨: {client.user}")

    try:
        await send_ranking()
    except Exception as e:
        print("❌ 에러 발생:", e)

    # 👉 실행 끝나면 종료 (자동화 핵심)
    await client.close()
    print("🛑 봇 종료")


async def main():
    if not TOKEN:
        print("❌ DISCORD_TOKEN 없음")
        return

    if not os.environ.get("GOOGLE_CREDENTIALS"):
        print("❌ GOOGLE_CREDENTIALS 없음")
        return

    print("🚀 봇 시작")
    await client.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())