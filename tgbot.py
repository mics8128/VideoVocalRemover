import os
from dotenv import load_dotenv
from pytube import YouTube
import demucs.separate
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackContext
import shlex

from lib.utils import is_youtube_url

# load envs
load_dotenv()
tg_token = os.getenv('TG_TOKEN')

# 路徑們
current_path = os.path.dirname(__file__)
temp_path = os.path.join(current_path, 'temp')

# outputs
output_path = os.path.join(current_path, 'output')
no_vocals_path = os.path.join(output_path, 'NoVocals')
original_path = os.path.join(output_path, 'Original')


async def removeVoice(update: Update, _: CallbackContext) -> None:
    url = update.message.text
    if not is_youtube_url(url):
        await update.message.reply_text(f'Usage: /removeVoice <youtube_url>')
        return

    processingMsg = await update.message.reply_text(f'影片處理中... 請稍後')

    # 使用 pytube 下載影片
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()

    # 下載影片
    video_file = stream.download(output_path=temp_path)

    # 取得影片檔案名稱 (不包含副檔名)
    video_name = os.path.splitext(os.path.basename(video_file))[0]

    # 伴奏檔案名稱
    no_vocals_file = os.path.join(
        temp_path, f"htdemucs_ft", f"{video_name}", f"no_vocals.mp3")

    # 分割伴奏 (如果沒有)
    if not os.path.exists(no_vocals_file):
        demucs.separate.main(shlex.split(
            f"--mp3 --two-stems vocals -n htdemucs_ft -d cuda \"{video_file}\" -o \"{temp_path}\""))

    # 輸出
    output_no_vocals_file = os.path.join(
        no_vocals_path, f"{video_name}_NoVocals.mp4")

    # 聲音用 no_vocals_file 影片用 video_file 輸出到 output_no_vocals_file
    if not os.path.exists(output_no_vocals_file):
        os.system(
            f"ffmpeg -i \"{video_file}\" -i \"{no_vocals_file}\" -map 1:a -map 0:v -c:v copy \"{output_no_vocals_file}\"")

    # 上傳檔案
    await update.message.reply_video(open(output_no_vocals_file, 'rb'), write_timeout=300)

    # 刪除 Processing 訊息
    await processingMsg.delete()


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Usage: paste a youtube.')

app = ApplicationBuilder().token(tg_token).build()
app.add_handler(MessageHandler(filters.TEXT, removeVoice))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("start", help))
app.run_polling()
