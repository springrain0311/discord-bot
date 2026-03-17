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

embed.set_footer(text="매주 목요일 00:00 자동 갱신 🌙")