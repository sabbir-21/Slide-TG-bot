from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
import shutil
import requests
import os
import re
from bs4 import BeautifulSoup as bs
import time
from datetime import timedelta
import math
import base64
from progress_bar import progress, TimeFormatter, humanbytes
from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')
workers = int(os.environ.get('WORKERS'))
api = int(os.environ.get('API_KEY'))
hash = os.environ.get('API_HASH')
chnnl = os.environ.get('CHANNEL_URL')
site = os.environ.get('SITE_URL')
BOT_URL = os.environ.get('BOT_URL')

app = Client("sabbir21", bot_token=bot_token, api_id=api, api_hash=hash)
#, workers=workers

@app.on_message(filters.command('start'))
def start(client, message):
    kb = [[InlineKeyboardButton('URL 🛡', url=chnnl),InlineKeyboardButton('Site 🔰', url=site)]]
    reply_markup = InlineKeyboardMarkup(kb)
    app.send_message(chat_id=message.from_user.id, text=f"Hello there, I am **Slideshare Downloader Bot**.\nI can download Slideshare PDF.\n\n"
                          "__**Developer :**__ __@sabbir21__\n"
                          "__**Language :**__ __Python__\n"
                          "__**Framework :**__ __🔥 Pyrogram__",
                     parse_mode='md',
                     reply_markup=reply_markup)

@app.on_message(filters.command('help'))
def help(client, message):
    kb = [[InlineKeyboardButton('URL 🛡', url=chnnl),InlineKeyboardButton('Site 🔰', url=site)]]
    reply_markup = InlineKeyboardMarkup(kb)
    app.send_message(chat_id=message.from_user.id, text=f"Hello there, I am **Slideshare Downloader Bot**.\nI can download any Slideshare PDF from link. Limited to 50MB file\n\n"
                                            "__Send me a Slideshare url__",
                     parse_mode='md',
                     reply_markup=reply_markup)

@app.on_message((filters.regex("http://")|filters.regex("https://")) & (filters.regex('slideshare')))
def slideshare_dl(client, message):
    a = app.send_message(chat_id=message.chat.id,
                         text='__Downloading File... __',
                         parse_mode='md')
    link = re.findall(r'\bhttps?://.*[(slideshare)]\S+', message.text)[0]
    link = link.split("?")[0]

    apil = f"https://www.slidesharedownloader.com/slideshareappiiiippg/pdfapi.php?url={link}"
    directory = str(round(time.time()))
    os.mkdir(directory)
    filename = link.split("/")[-1]+".pdf"
    r = requests.get(apil, allow_redirects=True)
    open(f'{directory}/{filename}', 'wb').write(r.content)

    a.edit(f'__Downloaded file!\n'
            f'Uploading to Telegram Now ⏳__')
    start = time.time()
    title = filename
    app.send_document(chat_id=message.chat.id,
                        document=f"{directory}/{filename}",
                        caption=f"**File :** __{filename}__\n"
                        f"__Uploaded by @{BOT_URL}__",
                        file_name=f"{directory}",
                        parse_mode='md',
                        progress=progress,
                        progress_args=(a, start, title))
    a.delete()
    try:
        shutil.rmtree(directory)
    except:
        pass

app.run()