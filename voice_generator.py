##import subprocess
import re

from gtts import gTTS

# remove_custom_emoji
# 絵文字IDは読み上げない
def remove_custom_emoji(inputText):
    pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'    # カスタム絵文字のパターン
    return re.sub(pattern,'えもじ',inputText)   # 置換処理

# urlAbb
# URLなら省略
def urlAbb(inputText):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return re.sub(pattern,'URLは省略します',inputText)   # 置換処理

def blackListWord(inputText):
    pattern = "アレクサ"
    inputText = re.sub(pattern,'',inputText)   # 置換処理
    pattern = "あれくさ"
    inputText = re.sub(pattern,'',inputText)   # 置換処理
    return inputText

def remove_command(inputText):
    pattern = r'^\/.*'
    return re.sub(pattern,'',inputText)   # 置換処理

def user_custam(inputText):
    f = open('./text/dic.txt', 'r')
    lines = f.readlines()

    for line in lines:
        pattern = line.strip().split(',')
        if pattern[0] in inputText:
            inputText = inputText.replace(pattern[0], pattern[1])
            print('置換後のtext:'+inputText)
            break
        else:
            line = f.readline()
    return inputText

# message.contentをテキストファイルに書き込み
def creat_sound(inputText):
    # message.contentをテキストファイルに書き込み
    inputText = remove_custom_emoji(inputText)   # 絵文字IDは読み上げない
    inputText = urlAbb(inputText)   # URLなら省略
    inputText = blackListWord(inputText)   # 禁止単語を省略
    inputText = remove_command(inputText)   # コマンドを省略
    inputText = user_custam(inputText)   # コマンドを省略

    tts = gTTS(text=inputText, lang='ja')
    tts.save('./output.mp3')

    return True

if __name__ == '__main__':
    creat_WAV('テスト')