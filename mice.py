import discord
from discord.ext import commands, tasks
from discord import app_commands
import datetime
from flask import Flask
from threading import Thread
import os
import aiohttp
from dotenv import load_dotenv

# 讀取環境變數
load_dotenv() 
TOKEN = os.getenv('TOKEN')

# --- Flask Keep-Alive 區塊 ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Render 必須綁定到環境變數中的 PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 機器人主程式類別 ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="$", intents=intents)

    async def setup_hook(self):
        # 啟動自動 Ping 任務
        self.auto_ping.start()
        # 同步 Slash 指令
        await self.tree.sync()
        print("Slash 指令已同步")

    # 每 10 分鐘自動 Ping 自己，防止 Render 休眠
    @tasks.loop(minutes=10)
    async def auto_ping(self):
        # 修正：直接從環境變數抓網址，或手動填入
        url = "https://new-discord-mice-bot.onrender.com" 
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    print(f"自補給成功！狀態碼: {response.status}")
            except Exception as e:
                print(f"Ping 自己時發生錯誤: {e}")

    @auto_ping.before_loop
    async def before_ping(self):
        await self.wait_until_ready()

# 實體化機器人
bot = MyBot()

# --- 指令與事件 ---

@bot.tree.command(name="unmute", description="慈善家請睜眼 你要幫助的是誰")
@app_commands.describe(member="要解除禁言的人")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    try:
        await member.timeout(None)
        await interaction.response.send_message(f"{interaction.user.mention} 已拯救 {member.mention} 的言論自由")
        await member.edit(nick=None)
    except discord.Forbidden:
        await interaction.response.send_message("官位不夠大 請前往儲值口充值")
    except Exception:
        await interaction.response.send_message("問就是cloudflare在搞")

@bot.event
async def on_ready():
    print(f"已登入：{bot.user}")
    
    # 遍歷機器人加入的所有伺服器
    for guild in bot.guilds:
        # 檢查該伺服器是否已經有名為「留友看勞鼠」的頻道
        channel = discord.utils.get(guild.text_channels, name="留友看勞鼠")
        
        if channel is None:
            try:
                # 如果找不到，就創建一個
                channel = await guild.create_text_channel("留友看勞鼠")
                await channel.send("# 起司 :cheese:")
                print(f"成功在 {guild.name} 補建頻道")
            except discord.Forbidden:
                print(f"在 {guild.name} 權限不足，無法補建頻道")
            except Exception as e:
                print(f"在 {guild.name} 發生錯誤：{e}")
        else:
            # 如果頻道已經存在，可以選擇要不要補發訊息（選配）
            try:
                await channel.send("# 起司 :cheese:")
                print(f"{guild.name} 的頻道已存在，跳過建立")
            except:
                pass

    # 最後同步 Slash 指令
    await bot.tree.sync()
    print("所有伺服器頻道檢查完畢，Slash 指令已同步！")


@bot.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.text_channels, name="留友看勞鼠")
    if channel is None:
        try:
            channel = await guild.create_text_channel("留友看勞鼠")
            await channel.send("# 起司 :cheese:")
        except Exception as e:
            print(f"建立頻道失敗：{e}")
    else:
        try:
            await channel.send("# 起司 :cheese:")
        except:
            pass

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == "留友看勞鼠":
        print(f"{message.guild.name} {message.author}: {message.content}")
        
        embed = discord.Embed(
            title="勞鼠\n",
            description=f"{message.author.mention} 是可愛的小勞鼠",
            color=discord.Colour.random(),
        )
        await message.channel.send(embed=embed)
        
        # 發送 GIF
        await message.channel.send("https://klipy.com/gifs/-24579")
        
        # 改暱稱
        try:
            await message.author.edit(nick="勞鼠")
        except discord.Forbidden:
            await message.channel.send("# 嗚嗚嗚管理員濫權")
            
        # 禁言 10 分鐘
        try:
            duration = datetime.timedelta(minutes=10)
            await message.author.timeout(duration)
        except:
            await message.channel.send("# 羨慕了好大的官威")
    else:
        if message.content == "勞鼠":
            await message.channel.send("吱吱")
        if message.content == "老鼠":
            await message.channel.send("你才老鼠")
        if message.content == "mice" or message.content == "mouse" :
            await message.channel.send("ん？(要素察覺")
    await bot.process_commands(message)

# --- 啟動 ---
if __name__ == "__main__":
    keep_alive()
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤：找不到 TOKEN 環境變數！")