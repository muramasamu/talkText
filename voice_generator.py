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
    return re.sub(pattern,'URLは省略するのデス！',inputText)   # 置換処理

def blackListWord(inputText):
    pattern = "アレクサ"
    inputText = re.sub(pattern,'',inputText)   # 置換処理
    pattern = "あれくさ"
    inputText = re.sub(pattern,'',inputText)   # 置換処理
    return inputText

    #inputText.encode('shift_jis')
    #inputText = inputText.replace('アレクサ', '', regex=True)
    #inputText = inputText.replace('あれくさ', '', regex=True)
    #return inputText

# creat_WAV
# message.contentをテキストファイルに書き込み
def creat_sound(projectMainPath,inputText):
    # message.contentをテキストファイルに書き込み
    inputText = remove_custom_emoji(inputText)   # 絵文字IDは読み上げない
    inputText = urlAbb(inputText)   # URLなら省略
    inputText = blackListWord(inputText)   # URLなら省略

    tts = gTTS(text=inputText, lang='ja')
    tts.save('./output.mp3')

    return True

if __name__ == '__main__':
    creat_WAV('テスト')