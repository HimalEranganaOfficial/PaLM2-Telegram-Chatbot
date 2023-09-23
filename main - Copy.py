import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

global conversation
conversation = {}
global conv
conv = ''

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

palm.configure(api_key='YOUR_PALM_API_KEY')
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

async def reset(update:Update, context: ContextTypes.DEFAULT_TYPE):
  global conversation
  del(conversation)
  conversation = {}
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Successfully cleared the recent chat meomry!")

async def handle_message(update: Update, context: CallbackContext):
  user_message = update.message.text
  global conv
  try:
    prompt = "Can you respond to the following conversation?\n"+str(conv)+"\nMe: "+str(user_message)
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=4000,
    )
    print("Answer> " + str(completion.result))
    result = str(completion.result)
    conversation[str(user_message)] = str(result)
    fconversation = []
    for question, answer in conversation.items():
      fconversation.append(f"Me: {question}\nYou: {answer}")
    conv = (str('\n'.join(map(str, fconversation))))
    await context.bot.send_message(chat_id=update.effective_chat.id,text=result)
    if (33554432 < len(str(conversation))):
      await context.bot.send_message(chat_id=update.effective_chat.id,text="You are reaching the bot memory usage limit...! Use /reset command to start new discussion.")
  except Exception as e2:
    print(
        "An error Occured when Getting user responce and Generating Replies...!\n"+str(e2)
    )


if __name__ == '__main__':
  application = ApplicationBuilder().token(
      'YOUR_TELEGRAM_BOT_API_KEY').build()

  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)

  reset_handler = CommandHandler('reset', reset)
  application.add_handler(reset_handler)

  message_handler = MessageHandler(filters.TEXT & (~filters.Command()),handle_message)
  application.add_handler(message_handler)

  application.run_polling()