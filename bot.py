# bot.py
import os
from pyrogram import Client, filters
import youtube_dl

TOKEN = os.getenv("TOKEN")
API_ID = int(os.getenv("APP_ID"))
API_HASH = os.getenv("APP_HASH")

app = Client("my_bot", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Привет! Отправь мне ссылку на YouTube, и я скачаю видео.")

@app.on_message(filters.private & filters.text)
async def download_video(client, message):
    url = message.text.strip()
    await message.reply("Скачиваю видео, подожди...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)

        await message.reply_video(video_file)
        os.remove(video_file)

    except Exception as e:
        await message.reply(f"Ошибка при скачивании: {e}")

if __name__ == "__main__":
    app.run()
