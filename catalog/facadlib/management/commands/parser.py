import os
import asyncio  # Add this line
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import speech_recognition as sr
import pydub
from facadlib.models import Advertisement
from asgiref.sync import sync_to_async
from transcribe_anything.api import transcribe




def get_html(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    response = driver.page_source
    driver.quit()
    return response

def get_data(html):
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_ads(soup):
    div_class = 'xh8yej3'
    ads = soup.find_all('div', class_=div_class)
    ads_video = []
    for ad in ads:
        ad_video = ad.find('video')
        if ad_video:
            try:
                if 'Library ID:' in ad.find_all('span')[0].text:
                    ad_id = ad.find_all('span')[0].text.split('Library ID: ')[1]
            except:
                pass
            url = ad_video['src']
            ads_video.append((url, ad_id))
    ads_video = set(ads_video)
    return ads_video

def download_video(url:str, ad_id:str):
    r = requests
    response = r.get(url)
    with open(f'{ad_id}.mp4', 'wb') as file:
        file.write(response.content)
    return f'{ad_id}.mp4'

def convert_to_audio(file:str):
   # convert to audio to wav
    audio = pydub.AudioSegment.from_file(file, format='mp4')
    audio.export(f'{file}.wav', format='wav')
    return f'{file}.wav'

def recognize_audio(file:str):
    #recognise with pocketsphinx
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    try:
        text = r.recognize_sphinx(audio)
        return text
    except Exception as e:
        print(e)
        return None
    
def recognize_audio_2(file_or_link:str):
    transcribe(
        url_or_file=f"{file_or_link}",
        output_dir="./",
    )

def recognize_audio_3(audio_data, language='en-US') -> str:
    """
    Transcribes audio data to text using Google's speech recognition API.
    """
    with sr.AudioFile(audio_data) as source:
        audio_data_r = sr.Recognizer().record(source)
        r = sr.Recognizer()
        text = r.recognize_google(audio_data_r, language=language)
    return text

async def main(main_url):
    
    html = get_html(main_url)
    soup = get_data(html)
    ads = get_ads(soup)
    for ad in ads:
        url, ad_id = ad
        exist_id = await sync_to_async(Advertisement.objects.filter(ad_id=ad_id).exists)()
        if exist_id:
            continue
        else:
                
            file = download_video(url, ad_id)
            audio = convert_to_audio(file)
            text = recognize_audio_3(audio)
            if text:
                exist_text = await sync_to_async(Advertisement.objects.filter(ad_id=ad_id).exists)()
                if exist_text:
                    continue
                await sync_to_async(ad_create)(main_url.strip('view_all_page_id=')[-1],text, ad_id, url)
    clean_up(ads)

def ad_create(main_id, text, ad_id, main_url):
    ad = Advertisement.objects.create(main_id=main_id, text=text, ad_id=ad_id, link=main_url)
    ad.save()

def clean_up(ads):
    for ad in ads:
        url, ad_id = ad
        file = f'{ad_id}.mp4'
        audio = f'{file}.wav'
        os.remove(file)
        os.remove(audio)


if __name__ == '__main__':
    # main()
    pass

class Command(BaseCommand):
    help = 'Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bot is running'))
        asyncio.run(main('https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&media_type=all&search_type=page&view_all_page_id=108565685567156'))
        return 0