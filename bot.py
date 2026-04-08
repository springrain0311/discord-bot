import discord
import gspread
import os
import asyncio
import json
import datetime
import sys
from oauth2client.service_account import ServiceAccountCredentials

print("🔥 실행 시작")
sys.stdout.flush()

# 🔐 환경변수
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# 🔐 구글 인증
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

print("📡 구글 인증 시도")
sys.stdout.flush()

creds_dict = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gc = gspread.authorize(creds)

print("✅ 구글 인증 완료")
sys.stdout.flush()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def send_ranking():
    print("🚀 랭킹 전송 시작")
    sys.stdout.flush()

    # 🔥 시간 체크 (핵심)
    now = datetime.datetime.now() + datetime.timedelta(hours=9)

    # 목요일만 실행
    if now.weekday() != 3:
        print("⏭ 목요일 아님 → 종료")
        return

    # 00:00 ~ 00:10 사이만 허용
    if now.hour != 0 or now.minute > 10:
        print("⏭ 00시 범위 아님 → 종료")
        return

    print("⏰ 전송 가능 시간")
    sys.stdout.flush()

    sheet = gc.open("봄비길드 수로랭킹")
    current_sheet = sheet.sheet1
    backup_sheet = sheet.get_worksheet(1)

    current_data = current_sheet.get_all_values()
    old_data = backup_sheet.get_all_values()

    # 🔥 중복 방지
    today = now.strftime("%Y-%m-%d")
    if old_data and old_data[0][0] == today:
        print("⏭ 이미 전송됨 → 종료")
        return

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
            change = ""

        ranking_text += f"{icon} **{rank}위** │ `{name}`{change}\n　　└ 💖 **{score:,}**\n\n"

    ranking_text += "━━━━━━━━━━━━━━━━━━\n\n"

    # 🌸 4~10
    for i in range(4, 11):
        rank = int(current_data[i][0])
        name = current_data[i][1]
        score = int(current_data[i][2])

        if name in old_rank:
            diff = old_rank[name] - rank
            change = f" ▲{diff}" if diff > 0 else f" ▼{abs(diff)}" if diff < 0 else ""
        else:
            change = ""

        ranking_text += f"🌸 {rank:>2}위 │ `{name}`{change} │ {score:,}\n"

    ranking_text += "\n"

    # ✨ 11~20
    for i in range(11, 21):
        rank = int(current_data[i][0])
        name = current_data[i][1]
        score = int(current_data[i][2])

        if name in old_rank:
            diff = old_rank[name] - rank
            change = f" ▲{diff}" if diff > 0 else f" ▼{abs(diff)}" if diff < 0 else ""
        else:
            change = ""

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
    sys.stdout.flush()

    # 🔥 백업 + 날짜 저장 (중복 방지용)
    backup_sheet.clear()

    new_backup = [[today]]
    new_backup.extend(current_data)

    backup_sheet.update(new_backup)

    print("📦 백업 완료")
    sys.stdout.flush()


@client.event
async def on_ready():
    print(f"✅ 로그인됨: {client.user}")
    sys.stdout.flush()

    await send_ranking()

    await client.close()
    print("🛑 봇 종료")
    sys.stdout.flush()


async def main():
    if not TOKEN:
        print("❌ TOKEN 없음")
        return

    print("🚀 봇 시작")
    sys.stdout.flush()

    await client.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
