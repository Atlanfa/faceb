import os
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
import asyncio
from facadlib.management.commands import parser
from facadlib.models import PagesToMonitor, Advertisement
from asgiref.sync import sync_to_async

API_TOKEN = '7303202007:AAEwra4kYK5cHfiF0W3fFYjgoka9BAlURWE'
CHAT_ID = '229058474'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply(f"Hi!\nI'm your bot!\nSend me a page url to monitor.\nYour chat id is {message.chat.id}")

@sync_to_async
def create_page(url):
    PagesToMonitor.objects.create(url=url)

@dp.message()
async def add_page_to_monitor(message: types.Message):
    page_url = message.text
    await create_page(page_url)
    await message.reply(f'Page {page_url} added to monitor.')

@sync_to_async
def get_all_pages():
    return list(PagesToMonitor.objects.all())


async def check_pages():
    print('Checking pages')
    pages = await get_all_pages()
    for page in pages:
        print(f'Checking page: {page.url}')
        await parser.main(page.url)
# if __name__ == '__main__':
#     
#     executor.start_polling(dp, skip_updates=True)

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_pages, 'interval', hours=0.01)
    scheduler.start()
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bot is running'))
        asyncio.run(main())
        return 0