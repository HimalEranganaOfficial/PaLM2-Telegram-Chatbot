import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

from subprocess import Popen, PIPE
import os
import pprint
try:
  import google.generativeai as palm
  from telegram import Update
  from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
  from asyncio import Queue
  from telegram import Bot
except Exception as e1:
  print("An error occured: " + str(e1) + "\n" +
        "Don't worry! We are triyng to fix the problem...!")
  del (e1)
  os.system("pip install google-generativeai")
  os.system("pip install python-telegram-bot")
  import google.generativeai as palm
  from telegram import Update
  from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

palm.configure(api_key='AIzaSyD2nUGOZ7R7eGTYSV6wGlTYddyypIRlYCo')
models = [
    m for m in palm.list_models()
    if 'generateText' in m.supported_generation_methods
]
model = models[0].name
print("Avilable Models> " + str(model))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text="Feel free to talk with me. You can tell anything to me!")


async def handle_message(update: Update, context: CallbackContext):
  user_message = update.message.text
  try:
    prompt = str(user_message)
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=1000,
    )
    print("Answer> " + str(completion.result))
    result = str(completion.result)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=result)
  except Exception:
    print(
        "An error Occured when Getting user responce and Generating Replies...!"
    )


if __name__ == '__main__':
  application = ApplicationBuilder().token(
      '6550674936:AAHpCGFadOcvbZYZ5U8tdbSHcJVhxNTWqpE').build()

  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)

  message_handler = MessageHandler(filters.TEXT & (~filters.Command()),
                                   handle_message)
  application.add_handler(message_handler)

  application.run_polling()
