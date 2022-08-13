from bs4 import *
import requests
import os
import time
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bs4 import BeautifulSoup
import shutil
from dotenv import load_dotenv
#img2pdf
from PIL import Image
from natsort import natsorted

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')
api = os.environ.get('API_KEY')
hash = os.environ.get('API_HASH')

webdl = Client("sabbir21", bot_token=bot_token, api_id=api, api_hash=hash)

@webdl.on_message(filters.command(["start"]))
async def start(_, message: Message):
    text = f"Hello , I am a slide downloader bot.\n\n__**Developer :**__ __@sabbir21__\n__**Language :**__ __Python__\n__**Framework :**__ __🔥 Pyrogram__"

    await message.reply_text(text=text, disable_web_page_preview=True, quote=True)

@webdl.on_message(filters.command(["help"]))
async def start(_, message: Message):
    text = f"To download slide, send a link." \
    "\nSend me any link for slide pdf."
    await message.reply_text(text=text, disable_web_page_preview=True, quote=True)

@webdl.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")) & (filters.regex('slideshare')))
async def scrapping(bot, message):
    txt = await message.reply_text("Validating Link", quote=True)
    try:
        url = re.findall(r'\bhttps?://.*[(slideshare)]\S+', message.text)[0]
        url = url.split("?")[0]
        folder_name = str(round(time.time()))
        filename = url.split("/")[-1]
        r = requests.get(url)
        await txt.edit(text=f"Downloading slide", disable_web_page_preview=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.findAll('img', attrs = {'srcset' : True})
        os.mkdir(folder_name)
        if len(images) != 0:
            for i, image in enumerate(images):
                image_link = image["srcset"].split(',')[-1].split(' ')[1]
                try:
                    r = requests.get(image_link).content
                    try:
                        r = str(r, 'utf-8')
                    except UnicodeDecodeError:
                        with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                            f.write(r)
                except:
                    pass
        await txt.edit(text=f"Uploading to telegram", disable_web_page_preview=True)
        #pdf making
        file_names = os.listdir(folder_name)
        file_names = natsorted(file_names)
        pdfimages = [Image.open(f"{folder_name}/{f}") for f in file_names]
        pdf_path = filename + '.pdf'
        pdfimages[0].save(pdf_path, "PDF" , resolution=100.0, save_all=True, append_images=pdfimages[1:])

        await message.reply_document(filename+".pdf", caption=f"**File:** {filename}.pdf\n"f"Developed by: **Sabbir Ahmed** @sabbir21", quote=True)
        
        await txt.delete()
    except Exception as error:
        print(error)
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return
    os.remove(filename+".pdf")
    shutil.rmtree(folder_name)

webdl.run()