import discord
import gspread
import os
import asyncio
import json
import datetime
from oauth2client.service_account import ServiceAccountCredentials

print("🔥 실행 시작")

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

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def send_ranking():
    print("🚀 랭킹 전송 시작")

    sheet = gc.open("봄비길드 수로랭킹")
    current_sheet = sheet.sheet1
    backup_sheet = sheet.get_worksheet(1)

    current_data = current_sheet.get_all_values()
    old_data = backup_sheet.get_all_values()

    # 🔥 오늘 날짜 (중복 방지용)
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # 👉 이미 보냈으면 종료
    if old_data and old_data[0][0] == today:
        print("⏭ 이미 전송됨 → 종료")
        return

    # 👉 이전 데이터 정리
    old_rank = {}
    for i in range(1, len(old_data)):
        if len(old_data[i]) >= 2:
            name = old_data[i][1]
            rank = int(old_data[i][0])
            old_rank[name] = rank

    ranking_text = ""

    # 🏆 TOP 3
    ranking_text += "🏆 **TOP 3**\n"
    for i in range(1, 4):
        rank = int(current_data[i][0])
        name = current_data[i][1]
        score = int(current_data[i][2])

        icons = ["🥇", "🥈", "🥉"]
        icon = icons[i-1]

        if name in old_rank:
            diff = old_rank[name] - rank
            change = f" ▲{diff}" if diff > 0 else f" ▼{abs(diff)}" if diff < 0 else ""
        else:
            change = " NEW"

        ranking_text += f"{icon} **{rank}위** │ `{name}`{change}\n　　└ 💖 **{score:,}**\n\n"

    ranking_text += "━━━━━━━━━━━━━━━━━━\n\n"

    # 🌸 4~10위
    for i in range(4, 11):
        rank = int(current_data[i][0])
        name = current_data[i][1]
        score = int(current_data[i][2])

        if name in old_rank:
            diff = old_rank[name] - rank
            change = f" ▲{diff}" if diff > 0 else f" ▼{abs(diff)}" if diff < 0 else ""
        else:
            change = " NEW"

        ranking_text += f"🌸 {rank:>2}위 │ `{name}`{change} │ {score:,}\n"

    ranking_text += "\n"

    # ✨ 11~20위
    for i in range(11, 21):
        rank = int(current_data[i][0])
        name = current_data[i][1]
        score = int(current_data[i][2])

        if name in old_rank:
            diff = old_rank[name] - rank
            change = f" ▲{diff}" if diff > 0 else f" ▼{abs(diff)}" if diff < 0 else ""
        else:
            change = " NEW"

        ranking_text += f"✨ {rank:>2}위 │ `{name}`{change} │ {score:,}\n"

    embed = discord.Embed(
        title="🌸 봄비길드 수로 랭킹 🌸",
        description=ranking_text,
        color=0xffb6c1
    )

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ 채널 못찾음")
        return

    await channel.send(embed=embed)
    print("✅ 메시지 전송 완료")

    # 🔥 백업 저장 (맨 위에 날짜 추가)
    backup_sheet.clear()

    new_backup = [[today]]
    new_backup.extend(current_data)

    backup_sheet.update(new_backup)

    print("📦 백업 완료")


@client.event
async def on_ready():
    print(f"✅ 로그인됨: {client.user}")

    await send_ranking()

    await client.close()
    print("🛑 봇 종료")


async def main():
    if not TOKEN:
        print("❌ TOKEN 없음")
        return

    print("🚀 봇 시작")
    await client.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
