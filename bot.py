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
client = commands.Bot(command_prefix='/')
client.remove_command("help")

# 作業ディレクトリをbot.pyが置いてあるディレクトリに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ユーザ辞書
user_dic = []

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
    helpFile = open('./text/help.txt', 'r', encoding='UTF-8')
    helpText = helpFile.read()
    await message.channel.send(helpText)
    helpFile.close()

@client.command()
async def dic(message):
    try:
        with open('./text/dic.txt', mode='r') as f:
            text = f.read()
            await message.channel.send('登録されている単語一覧\n'+'```' + text +'```')
    except:
        await message.channel.send('辞書データがありません')

@client.command()
async def addw(message, arg1, arg2):
    #既に登録されていないか確認

    hit = False
    try:
        print("確認処理")
        with open('./text/dic.txt', mode='r') as fr:
            print("open OK")
            lines = fr.readlines()
            print("1行読み込み")

            for line in lines:
                print(line)
                pattern = line.strip().split(',')
                print(pattern[0])
                print(pattern[1])
                if pattern[0] in arg1:
                    hit = True
                    await message.channel.send('`' + arg1+'`は既に`'+pattern[1]+'`として登録されています。')
                    break

    except:
        pass

    #登録処理 登録があればメッセージを表示
    if hit:
        await message.channel.send('登録処理は実施されませんでした。\n変更の場合は"rmw"コマンドで削除してから実行してください')

    else:
        with open('./text/dic.txt', mode='a') as fa:
            fa.write(arg1 + ',' + arg2 + '\n')
            print('dic.txtに書き込み：''\n'+ arg1 + ',' + arg2)
            await message.channel.send('`' + arg1+'` を `'+arg2+'` として登録しました')

@client.command()
async def rmw(message, arg1):
    hit = False
    with open("./text/dic.txt", "r") as f:
        lines = f.readlines()
        print(lines)
    with open("./text/dic.txt", "w") as f:
        for line in lines:
            pattern = line.strip().split(',')
            print(pattern)
            print(arg1)
            if arg1 != pattern[0]:
                f.write(line)
            else:
                hit = True
    if hit:
        await message.channel.send('`' + arg1+'` を辞書から削除しました')
    else:
        await message.channel.send('`' + arg1+'` は辞書に登録されていません')

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
            creat_sound(inputText)
            source = discord.FFmpegPCMAudio("output.mp3",options="-af atempo=1.5")
            message.guild.voice_client.play(source)
        else:
            pass
    await client.process_commands(message)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)