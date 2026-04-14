#<<<<<<< HEAD
import discord
from discord.ext import commands, tasks
from discord import app_commands
import datetime
from flask import Flask
from threading import Thread
import os
import aiohttp
from dotenv import load_dotenv

# 霈������啣��霈����
load_dotenv() 
TOKEN = os.getenv('TOKEN')

# --- Flask Keep-Alive ���憛� ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Render 敹����蝬�摰���啁�啣��霈���訾葉��� PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 璈���其犖銝餌��撘�憿���� ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="$", intents=intents)

    async def setup_hook(self):
        # ��������芸�� Ping 隞餃��
        self.auto_ping.start()
        # ���甇� Slash ���隞�
        await self.tree.sync()
        print("Slash ���隞文歇���甇�")

    # 瘥� 10 ��������芸�� Ping ��芸楛嚗���脫迫 Render 隡����
    @tasks.loop(minutes=10)
    async def auto_ping(self):
        # 靽格迤嚗���湔�亙����啣��霈���豢��蝬脣��嚗����������憛怠��
        url = "https://new-discord-mice-bot.onrender.com" 
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    print(f"��芾��蝯行�����嚗�������蝣�: {response.status}")
            except Exception as e:
                print(f"Ping ��芸楛�����潛����航炊: {e}")

    @auto_ping.before_loop
    async def before_ping(self):
        await self.wait_until_ready()

# 撖阡�����璈���其犖
bot = MyBot()

# --- ���隞方��鈭�隞� ---

@bot.tree.command(name="unmute", description="������摰嗉�������� 雿�閬�撟怠�拍����航狐")
@app_commands.describe(member="閬�閫���斤��閮����鈭�")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    try:
        await member.timeout(None)
        await interaction.response.send_message(f"{interaction.user.mention} 撌脫�舀�� {member.mention} ���閮�隢���芰��")
        await member.edit(nick=None)
    except discord.Forbidden:
        await interaction.response.send_message("摰�雿�銝�憭�憭� 隢����敺���脣�澆��������")
    except Exception:
        await interaction.response.send_message("���撠望�畚loudflare��冽��")

@bot.event
async def on_ready():
    print(f"撌脩�餃�伐��{bot.user}")
    
    # ���甇瑟����其犖�����亦��������隡箸�����
    for guild in bot.guilds:
        # 瑼Ｘ�亥府隡箸����冽�臬�血歇蝬���������箝��������������曌���������駁��
        channel = discord.utils.get(guild.text_channels, name="������������曌�")
        
        if channel is None:
            try:
                # 憒������曆����堆��撠勗�萄遣銝����
                channel = await guild.create_text_channel("������������曌�")
                await channel.send("# 韏瑕�� :cheese:")
                print(f"��������� {guild.name} 鋆�撱粹�駁��")
            except discord.Forbidden:
                print(f"��� {guild.name} 甈����銝�頞喉����⊥��鋆�撱粹�駁��")
            except Exception as e:
                print(f"��� {guild.name} ��潛����航炊嚗�{e}")
        else:
            # 憒������駁��撌脩��摮���剁����臭誑��豢��閬�銝�閬�鋆���潸����荔����賊��嚗�
            try:
                await channel.send("# 韏瑕�� :cheese:")
                print(f"{guild.name} �����駁��撌脣����剁��頝喲��撱箇��")
            except:
                pass

    # ���敺����甇� Slash ���隞�
    await bot.tree.sync()
    print("������隡箸����券�駁��瑼Ｘ�亙����ｇ��Slash ���隞文歇���甇伐��")


@bot.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.text_channels, name="������������曌�")
    if channel is None:
        try:
            channel = await guild.create_text_channel("������������曌�")
            await channel.send("# 韏瑕�� :cheese:")
        except Exception as e:
            print(f"撱箇����駁��憭望��嚗�{e}")
    else:
        try:
            await channel.send("# 韏瑕�� :cheese:")
        except:
            pass

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == "������������曌�":
        print(f"{message.guild.name} {message.author}: {message.content}")
        
        embed = discord.Embed(
            title="���曌�\n",
            description=f"{message.author.mention} ��臬�舀�����撠����曌�",
            color=discord.Colour.random(),
        )
        await message.channel.send(embed=embed)
        
        # ��潮�� GIF
        await message.channel.send("https://klipy.com/gifs/-24579")
        
        # ��寞�梁迂
        try:
            await message.author.edit(nick="���曌�")
        except discord.Forbidden:
            await message.channel.send("# ���������蝞∠����⊥翰甈�")
            
        # 蝳�閮� 10 ������
        try:
            duration = datetime.timedelta(minutes=10)
            await message.author.timeout(duration)
        except:
            await message.channel.send("# 蝢冽��鈭�憟賢之���摰�憡�")
    else:
        if message.content == "���曌�":
            await message.channel.send("��勗��")
        if message.content == "���曌�":
            await message.channel.send("雿�������曌�")
        if message.content == "mice" or message.content == "mouse" :
            await message.channel.send("���嚗�(閬�蝝�撖�閬�")
    await bot.process_commands(message)

# --- ������ ---
if __name__ == "__main__":
    keep_alive()
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("��航炊嚗���曆����� TOKEN ��啣��霈���賂��")
=======
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
            await message.channel.send("?？(要素察覺")
    await bot.process_commands(message)

# --- 啟動 ---
if __name__ == "__main__":
    keep_alive()
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤：找不到 TOKEN 環境變數！")
>>>>>>> e702d7d (first commit)
