import discord
import gspread
import os
import asyncio
import json
from oauth2client.service_account import ServiceAccountCredentials

# 🔐 환경변수 가져오기
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# 🔐 구글 인증 (Secrets에서 JSON 불러오기)
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
    print("랭킹 전송 시작")

    sheet = gc.open("봄비길드 수로랭킹").sheet1
    data = sheet.get_all_values()

    print("데이터 길이:", len(data))

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

    if channel is None:
        print("❌ 채널 못찾음")
        return

    await channel.send(embed=embed)
    print("✅ 메시지 전송 완료")


@client.event
async def on_ready():
    print(f"✅ 로그인됨: {client.user}")

    await send_ranking()

    # 👉 실행 끝나면 종료 (GitHub Actions용)
    await client.close()


async def main():
    if TOKEN is None:
        print("❌ DISCORD_TOKEN 없음")
        return

    await client.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())