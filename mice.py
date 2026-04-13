import discord
from discord.ext import commands
from discord import app_commands
import datetime
from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv # 如果你在本地測試，建議安裝 python-dotenv

# 讀取環境變數
load_dotenv() 
TOKEN = os.getenv('TOKEN')

# 建立一個簡單的網頁
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # 優先讀取 Render 給予的 Port，如果沒有則用 10000 (Render 預設)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()


intents = discord.Intents.default()
intents.message_content = True  # 必開
intents.members = True  # 視需求
client = discord.Client(intents = intents)

bot = commands.Bot(command_prefix = "$", intents = intents)

# Slash 指令（推薦）
@bot.tree.command(name="unmute", description="慈善家請睜眼 你要幫助的是誰")
@app_commands.describe(member="要解除禁言的人")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    try:
        # 將 timeout 設定為 None 即可立即解除禁言
        await member.timeout(None)

        await interaction.response.send_message(
            f"{interaction.user.mention} 已拯救 {member.mention} 的言論自由"
        )
    except discord.Forbidden:
        await interaction.response.send_message("官位不夠大 請前往儲值口充值")
    except Exception as e:
        await interaction.response.send_message(f"問就是cloudflare在搞")

@bot.event
async def on_ready():
    await bot.tree.sync()  # 同步 slash 指令
    print(f"已登入：{bot.user}")
    for guild in bot.guilds:  # 遍歷每一個伺服器
        channel = discord.utils.get(guild.text_channels, name="留友看勞鼠")
        if channel:
            await channel.send("# 起司:cheese:")
#TARGET_CHANNEL_ID = 123456789012345678  # 改成你的頻道ID

@bot.event
async def on_guild_join(guild):
    channel = discord.utils.get(await guild.text_channels, name="留友看勞鼠")
    if channel is None:
        try:
            # 建立文字頻道
            channel = await guild.create_text_channel("留友看勞鼠")

            # 傳送訊息
            await channel.send("#起司:cheese:")

            print(f"已在 {guild.name} 建立頻道")

        except Exception as e:
            print(f"建立頻道失敗：{e}")
    else:
        await channel.send("#起司:cheese:")
            

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == "留友看勞鼠":
        print(f"{message.guild.name} {message.author}: {message.content}")
        await message.channel.send(embed=discord.Embed(
            title= "勞鼠\n",
            description= f"{message.author} 是可愛的小勞鼠",
            color=discord.Colour.random(),
        ))
        gif_url = "https://klipy.com/gifs/-24579" 
        await message.channel.send(gif_url)
        try:
            await message.author.edit(nick="勞鼠")
        except discord.Forbidden:
            await message.channel.send("# 嗚嗚嗚管理員濫權")
        try:await message.author.edit(timed_out_until=discord.utils.utcnow() + datetime.timedelta(minutes=10))
        except:await message.channel.send("# 羨慕了好大的官威")
        #await message.channel.send(f'{member.name}已被設定超時時間，將在{minutes}分鐘後解除超時。')

    await bot.process_commands(message)


# 在檔案最後面
if __name__ == "__main__":
    keep_alive()  # 啟動網頁伺服器
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤：找不到 TOKEN 環境變數！")


