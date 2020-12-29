# インストールした discord.py を読み込む
import asyncio
import os
import subprocess

import ffmpeg
import discord
from playsound import playsound
from discord.ext import commands

from voice_generator import creat_sound


# 自分のBotのアクセストークン
TOKEN = os.environ['TOKEN']

# 接続に必要なオブジェクトを生成
#client = discord.Client()
client = commands.Bot(command_prefix='/')
client.remove_command("help")

#作業ディレクトリをbot.pyが置いてあるディレクトリに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))
projectMainPath = os.getcwd()

#msgclient = message.guild.voice_client

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    activity = discord.Activity(name='/help', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

@client.command()
async def join(message):
    print('#voicechannelを取得')
    vc = message.author.voice.channel
    print('#voicechannelに接続')
    await vc.connect()
    await message.channel.send('にゃーん！(接続しました)')

@client.command()
async def bye(message):
    print('#切断')
    await message.voice_client.disconnect()
    await message.channel.send('にゃーん...(切断しました)')

@client.command()
async def help(message):
    helpFile = open(projectMainPath + '/text/help.txt', 'r', encoding='UTF-8')
    helpText = helpFile.read()
    await message.channel.send(helpText)
    helpFile.close()

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
    # 「/inu」と発言したら「わん」が返る処理
    if message.content == '/inu':
        await message.channel.send('わん')

    if message.content.startswith('/'):
        pass

    else:
        if message.guild.voice_client:
            print(message.content)
            inputText = message.clean_content
            print(inputText)
            creat_sound(projectMainPath,inputText)
#            source = discord.FFmpegPCMAudio(executable = projectMainPath + "/open_jtalk/bin/ffmpeg/bin/ffmpeg.exe", source="output.wav")
##            source = discord.FFmpegPCMAudio("output.mp3")
            source = discord.FFmpegPCMAudio("output.mp3",options="-af atempo=1.5")
            message.guild.voice_client.play(source)
        else:
            pass
    await client.process_commands(message)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)