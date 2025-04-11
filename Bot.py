import logging
import feedparser
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
RSS_URL = "https://mipped.com/rss"  # можно заменить на другой раздел сайта

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /новости, чтобы получить свежие статьи с mipped.com")

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        await update.message.reply_text("Не удалось загрузить новости.")
        return

    for entry in feed.entries[:3]:
        title = entry.title
        link = entry.link
        await update.message.reply_text(f"**{title}**\n{link}", parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("новости", get_news))

    print("Бот запущен!")
    app.run_polling()
