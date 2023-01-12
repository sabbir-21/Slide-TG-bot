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
from tqdm.auto import tqdm

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')
api = os.environ.get('API_KEY')
hash = os.environ.get('API_HASH')

webdl = Client("sabbir21", bot_token=bot_token, api_id=api, api_hash=hash)

@webdl.on_message(filters.command(["start"]) )
async def start(_, message: Message):
    text = f"Hello , I am a slide downloader bot.\n\n__**Developer :**__ __@sabbir21__\n__**Language :**__ __Python__\n__**Framework :**__ __🔥 Pyrogram__"
    kb = [[InlineKeyboardButton('Channel 🛡', url="https://google.com/"),InlineKeyboardButton('Repo 🔰', url="https://github.com/")]]
    reply_markup = InlineKeyboardMarkup(kb)
    await message.reply_text(text=text, disable_web_page_preview=True, quote=True, reply_markup=reply_markup)

#@webdl.on_message(filters.command(["baq"]) & ~filters.chat("-1001325830273"))
@webdl.on_message(filters.command(["help"]))
async def help(_, message: Message):
    text = f"To download slide, send a link." \
    "\nSend me any link for slide pdf."
    await message.reply_text(text=text, disable_web_page_preview=True, quote=True)

#@webdl.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")) & (filters.regex('slideshare')) & filters.user(admin) & filters.private)


@webdl.on_message(filters.command(["send"]))
async def anydl(bot, message):
    txt = await message.reply_text("Sending Custom file", quote=True)
    try:
        
        custom = message.text.split("send ")[1]
        #custom = str(custom)
        await message.reply_document(custom, caption=f"File: {custom} \n"f"Developed by: **Sabbir Ahmed** @sabbir21", quote=True)
        await txt.delete()
    except Exception as error:
        print(error)
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return



@webdl.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")) & (filters.regex('slideshare')))
async def slideshare(bot, message):
    txt = await message.reply_text("Slideshare Link Detected", quote=True)
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
        file_names = os.listdir(folder_name) #make folder
        file_names = natsorted(file_names)
        pdfimages = [Image.open(f"{folder_name}/{f}") for f in file_names]
        pdf_path = filename + '.pdf'
        pdfimages[0].save(pdf_path, "PDF" , resolution=100.0, save_all=True, append_images=pdfimages[1:])

        #await message.reply_document(filename+".pdf", caption=f"**File:** {filename}.pdf\nUpload requested by {message.chat.first_name}\n"f"Developed by: **Sabbir Ahmed** @sabbir21", quote=True)
        await message.reply_document(filename+".pdf", caption=f"**File:** {filename}.pdf\n"f"Developed by: **Sabbir Ahmed** @sabbir21", quote=True)
        await txt.delete()
        #text parse
        
        file_write = open(filename+'.txt', 'a+', encoding="utf-8")
        for yy in soup.find_all('ol'):
            file_write.write(f"{yy.text}\n\n")
        file_write.close()
        await message.reply_document(f'{filename}.txt', caption=f"**Text Contents:** {filename}.txt\n"f"Developed by: **Sabbir Ahmed** @sabbir21", quote=True)
        
        try:
            shutil.rmtree(folder_name)
            os.remove(filename+".pdf")
            os.remove(filename+".txt")
            
        except: pass
    except Exception as error:
        print(error)
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        #await txt.delete()
        try:
            shutil.rmtree(folder_name)
            os.remove(filename+".pdf")
            os.remove(filename+".txt")
            
        except: pass
        return
    

@webdl.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")) & (filters.regex('slideplayer')))
async def slideplayer(bot, message):
    txt2 = await message.reply_text("Slideplayer Link Detected", quote=True)
    try:
        url = re.findall(r'\bhttps?://.*[(slideplayer)]\S+', message.text)[0]
        url = url.split("?")[0]
        folder_name = str(round(time.time()))
        filename = url.split("/")[-2]
        r = requests.get(url)
        await txt2.edit(text=f"Downloading from slideplayer", disable_web_page_preview=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.findAll('img', attrs = {'srcset' : True})
        os.mkdir(folder_name)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        #images = soup.find_all('img')
        #loop fn
        i = 0
        for ns in soup.find_all('noscript'):
            images = ns.img['src'].split("//")[1]
            images = "http://" + images
            i += 1
            r = requests.get(images).content
            open(f"{folder_name}/images_{i}.jpg", "wb+").write(r)
        await txt2.edit(text=f"Uploading to telegram", disable_web_page_preview=True)
        #pdf making
        file_names = os.listdir(folder_name) #make folder
        file_names = natsorted(file_names)
        pdfimages = [Image.open(f"{folder_name}/{f}") for f in file_names]
        pdf_path = filename + '.pdf'
        pdfimages[0].save(pdf_path, "PDF" , resolution=100.0, save_all=True, append_images=pdfimages[1:])

        await message.reply_document(filename+".pdf", caption=f"**File:** {filename}.pdf\n"f"Developed by: **Sabbir Ahmed** @sabbir21", quote=True)
        await txt2.delete()
        try:
            shutil.rmtree(folder_name)
            os.remove(filename+".pdf")
        except: pass
    except Exception as error:
        print(error)
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt2.delete()
        try:
            shutil.rmtree(folder_name)
            os.remove(filename+".pdf")
        except: pass
        return
    

#slideserve
@webdl.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")) & (filters.regex('slideserve')))
async def slideserve(bot, message):
    txt2 = await message.reply_text("Slideserve Link Detected", quote=True)
    try:
        
        url = message.text
        #url = url.split("?")[0]
        folder_name = str(round(time.time()))
        filename = 'alu'
        r = requests.get(url)
        await txt2.edit(text=f"Downloading from slideserve", disable_web_page_preview=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        #images = soup.findAll('img', attrs = {'srcset' : True})
        os.mkdir(folder_name)
        #images = soup.find_all('img')
        #loop fn
        i=0
        for img in soup.find_all('a'):
            images = img.get('href').split("//")[1]
            images = "http://" + images
            i += 1
            r = requests.get(images).content
            open(f"{folder_name}/images_{i}.jpg", "wb+").write(r)
        await txt2.edit(text=f"Uploading to telegram", disable_web_page_preview=True)
        #pdf making
        
        file_names = os.listdir(folder_name) #make folder
        file_names = natsorted(file_names)
        pdfimages = [Image.open(f"{folder_name}/{f}") for f in file_names]
        pdf_path = filename + '.pdf'
        pdfimages[0].save(pdf_path, "PDF" , resolution=100.0, save_all=True, append_images=pdfimages[1:])
        
        await message.reply_document(filename+".pdf", caption=f"**File:** {filename}.pdf\n"f"Developed by: **Sabbir Ahmed** @sabbir21", quote=True)
        
        file_write = open(filename+'.txt', 'a+', encoding="utf-8")
        for yy in soup.find_all('ol'):
            file_write.write(yy.text+'\n\n')
        file_write.close()
        await message.reply_document(f'{filename}.txt', caption=f"**Text Contents:** {filename}.txt\n"f"Developed by: **Sabbir Ahmed** @sabbir21", quote=True)
        await txt2.delete()
        try:
            shutil.rmtree(folder_name)
            os.remove(filename+".pdf")
        except: pass
    except Exception as error:
        print(error)
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt2.delete()
        try:
            shutil.rmtree(folder_name)
            os.remove(filename+".pdf")
        except: pass
        return
    
#any dl fn
@webdl.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")))
async def anydl(bot, message):
    txt2 = await message.reply_text("Direct Link Detected", quote=True)
    try:

        url = re.findall(r'\bhttps?://.*\S+', message.text)[0]
        url = url.split("?")[0]
        #folder_name = str(round(time.time()))
        with requests.get(url, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            await txt2.edit(text=f"Downloading to the server", disable_web_page_preview=True)
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                with open(f"{os.path.basename(r.url)}", 'wb')as output:
                    shutil.copyfileobj(raw, output)
                    await txt2.edit(text=f"Uploading to telegram", disable_web_page_preview=True)
        await message.reply_document(output.name, caption=f"File Upload requested by {message.chat.username}\n"f"Developed by: **Sabbir Ahmed** @sabbir21", quote=True)
        #os.remove(output.name)
    except Exception as error:
        print(error)
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt2.delete()
        os.remove(output.name)
        return
    os.remove(output.name) 
     


#main fn run
webdl.run()
