import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import telegram

# OpenAI API Token
OPENAI_TOKEN = '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'

TOKEN = '6380285902:AAEGqAQNbpEw0UgnBLDfmG-IlV1RPSgxQ6I'
bot = telegram.Bot(token=TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def generate_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    response = openai_generate_response(message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def openai_generate_response(message):
    url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
    headers = {
        'Authorization': f'Bearer {OPENAI_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': message,
        'max_tokens': 50
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['text']
    else:
        return 'Something went wrong. Please try again later.'

if __name__ == 'main':
    application = ApplicationBuilder().token('').build()

    start_handler = CommandHandler('start', start)
    generate_response_handler = CommandHandler('generate', generate_response)

    application.add_handler(start_handler)
    application.add_handler(generate_response_handler)

    application.run_polling()