import asyncio
from telethon.sync import TelegramClient
import pandas as pd
from colorama import Fore, Style
import re
import datetime
import time
import smtplib
from email.message import EmailMessage
import dbOPR

api_id = "apiID"
api_hash = "apiHash"
phone = "number"

channelList=("OrnekKanalID1","OrnekKanalID2")
keywords = ["aranacak","ara","kelime"]

def htmlMail(val,channel):
    EMAIL_ADDRESS = ''
    EMAIL_PASSWORD = ''
    TO_EMAIL=''
    msg = EmailMessage()
    msg['Subject'] = f'"{channel}" Kanalında Eşleşmeler Bulundu'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg.set_content(f"{val}", subtype='html')
 
    with smtplib.SMTP('smtp.example.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        smtp.quit()
def contentConvertHTML(content):
    df = pd.DataFrame(content, columns=['UTC','Text','Message URL'])
    dfHTML = df.to_html(index=False)
    if content:
        return dfHTML
    else:
        pass
async def scrape_channel_content(channel_name):
    async with TelegramClient(phone, api_id, api_hash) as client:
        def inputControl(vals,postDate, control_list):
            cleanText=inputCleaner(vals)
            pattern = r'\b(?:' + '|'.join(map(re.escape, control_list)) + r')\b'
            match = re.findall(pattern, cleanText, flags=re.IGNORECASE)
            vtQuery= dbOPR.inputSearch(cleanText)
            if match and not vtQuery:
                dbOPR.inputSave(postDate,cleanText,message_url)
                content.append((postDate,cleanText, message_url))
        def inputCleaner(vals):
            inputCleaner=re.sub(r'[^\x00-\x7F]+', '', vals)
            return inputCleaner
        def timeControl(postDate):
            postDate=str(postDate)
            today=datetime.datetime.today()
            lastTwentyFourHours=today - datetime.timedelta(hours=24)
            lastTwentyFourHours=lastTwentyFourHours.strftime("%Y-%m-%d %H:%M:%S")
            postDate=datetime.datetime.fromisoformat(postDate)
            postDate=postDate.strftime("%Y-%m-%d %H:%M:%S")
            if postDate >= lastTwentyFourHours:
                return True
            else:
                return False
        try:
            entity = await client.get_entity(channel_name)
            content = []
            post_count = 0

            async for post in client.iter_messages(entity):
                time.sleep(0.63)
                text = post.text
                postDate = post.date
                message_url = f"https://t.me/{channel_name}/{post.id}"
                if timeControl(postDate):
                    inputControl(text,postDate,keywords)
                    post_count += 1
                else:
                    break
                if post_count % 10 == 0:
                    print(
                        f"{Fore.WHITE}{post_count} Posts scraped in {Fore.LIGHTYELLOW_EX}{channel_name}{Style.RESET_ALL}")
            return content

        except Exception as e:
            print(f"An error occurred: {Fore.RED}{e}{Style.RESET_ALL}")
            return []

async def main():    
    while True:
        try:
            for channel in channelList:
                print(f'Scraping content from {Fore.LIGHTYELLOW_EX}{channel}{Style.RESET_ALL}...')
                content = await scrape_channel_content(channel)
                htmlContent = contentConvertHTML(content)
                if htmlContent != None:
                    htmlMail(htmlContent,channel)
                    
        except Exception as e:
            print(f"An error occurred: {Fore.RED}{e}{Style.RESET_ALL}")
        time.sleep(300)

if __name__ == '__main__':
    asyncio.run(main())