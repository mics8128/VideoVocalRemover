import os
from dotenv import load_dotenv

# load envs
load_dotenv()
tg_token = os.getenv('TG_TOKEN')

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def removeVoice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 0:
        await update.message.reply_text(f'Usage: /removeVoice <youtube_url>')
        return
    url = context.args[0]


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Usage: /removeVoice <youtube_url>')

app = ApplicationBuilder().token(tg_token).build()
app.add_handler(CommandHandler("removeVoice", removeVoice))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("start", help))
app.run_polling()