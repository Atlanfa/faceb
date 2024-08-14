from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Advertisement
from aiogram import Bot
import asyncio

API_TOKEN = '7303202007:AAEwra4kYK5cHfiF0W3fFYjgoka9BAlURWE'
CHAT_ID = '229058474'

bot = Bot(token=API_TOKEN)

@receiver(post_save, sender=Advertisement)
def advertisement_created(sender, instance, created, **kwargs):
    if created:
        message = f'New advertisement found: {instance.link}'
        # asyncio.run(send_message(message))
        #split message to avoid telegram bot error
        messages = []
        messages.append(message)
        messages += [instance.text[i:i+4096] for i in range(0, len(instance.text), 4096)]
        loop = asyncio.new_event_loop()
        loop.run_until_complete(send_message(messages))


        print('Message sent')

async def send_message(messages: list):
    for message in messages:
        await bot.send_message(chat_id=CHAT_ID, text=message)