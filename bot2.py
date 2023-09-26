import logging
import json
import telegram
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler

# Установите токен бота, полученный от BotFather
TOKEN = '6380285902:AAEGqAQNbpEw0UgnBLDfmG-IlV1RPSgxQ6I'
bot = telegram.Bot(token=TOKEN)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Словарь для хранения соединений между пользователями и психологами
connections = {}

# Константы для состояний разговора
CHAT_REQUESTED, CHAT_ESTABLISHED = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Создаем клавиатуру с кнопками для всех команд
    commands_keyboard = [
        ["/learn", "/diary"],
        ["/crisis", "/tips"],
        ["/groupsupport", "/progress"],
        ["/express"]
    ]

    reply_markup = ReplyKeyboardMarkup(commands_keyboard, resize_keyboard=True)
    await update.message.reply_text("Добро пожаловать! Чем я могу вам помочь?", reply_markup=reply_markup)


async def learn(update, context):
    # Добавьте здесь код для предоставления образовательных материалов
    await update.message.reply_text(
        "Здесь вы можете получить образовательные материалы о психологическом благополучии и стратегиях управления эмоциями.")


async def diary(update, context):
    # Добавьте здесь код для ведения дневника настроения
    await update.message.reply_text(
        "Вы можете вести дневник настроения, записывая свои эмоции и состояние. Просто отправьте сообщение с вашей записью.")


async def crisis(update, context):
    # Добавьте здесь код для предоставления контактов экстренной психологической помощи
    await update.message.reply_text(
        "Если у вас кризисная ситуация, пожалуйста, обратитесь за помощью по следующим контактам:\n"
        "1.[Кирилл - Вор Эмоций] - Телефон: +375292369785\n"
        "2.[Telegram] - https://t.me/squidtwister\n"
    )


async def tips(update, context):
    # Добавьте здесь код для предоставления советов и упражнений
    await update.message.reply_text(
        "Вот несколько советов и упражнений, которые могут вам помочь управлять стрессом:\n"
        "1. Проводите время на свежем воздухе и занимайтесь физической активностью.\n"
        "2. Практикуйте глубокое дыхание и медитацию.\n"
        "3. Ведите дневник настроения и обращайте внимание на свои эмоции.\n"
        "4. Поговорите с близкими людьми о своих чувствах и проблемах.\n"
        "5. Попробуйте творческие методы выражения, такие как рисование или музыка.")


async def group_support(update, context):
    # Добавьте здесь код для создания группового чата для поддержки
    await update.message.reply_text(
        "Вы можете создать групповой чат для поддержки с другими пользователями, которые также ищут поддержку.")


async def progress(update, context):
    # Добавьте здесь код для отслеживания прогресса пользователя
    await update.message.reply_text(
        "Вы можете отслеживать свой психологический прогресс и получать аналитику о вашем состоянии.")


async def express(update, context):
    # Добавьте здесь код для творческого выражения эмоций
    await update.message.reply_text(
        "Творческое выражение эмоций может быть замечательным способом обработки эмоций. Попробуйте рисовать, писать стихи, играть на музыкальных инструментах или заниматься чем-то другим, что вас вдохновляет.")


async def help_command(update, context):
    await update.message.reply_text(
        "Я здесь, чтобы помочь вам управлять стрессом, тревожностью и депрессией. Вот что я могу сделать:\n\n"
        "/chat - Начать анонимный чат с психологом\n"
        "/learn - Получить образовательные материалы\n"
        "/diary - Вести дневник настроения\n"
        "/crisis - Получить контакты экстренной помощи\n"
        "/tips - Получить советы и упражнения\n"
        "/groupsupport - Создать групповой чат для поддержки\n"
        "/progress - Просмотреть свой прогресс\n"
        "/express - Творчески выразить свои эмоции")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in connections and connections[user_id] != '':
        await update.message.reply_text("Вы уже находитесь в чате с психологом.")
    else:
        psychologist_id = '461421538'  # Замените на идентификатор вашего психолога
        await context.bot.send_message(
            chat_id=psychologist_id,
            text=f"Пользователь {user_id} хочет начать анонимный чат. Примите запрос, введя /accept {user_id}"
        )
        connections[user_id] = ''

        await update.message.reply_text("Запрос на чат отправлен психологу.")


async def accept_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    psychologist_id = update.effective_user.id

    if context.args:
        user_id = context.args[0]

        if user_id not in connections:
            connections[user_id] = psychologist_id
            await context.bot.send_message(
                chat_id=user_id,
                text="Ваш запрос на чат был принят. Вы начали анонимный чат с психологом. Пожалуйста, напишите ваш вопрос или проблему."
            )
            await context.bot.send_message(
                chat_id=psychologist_id,
                text=f"Вы приняли запрос на чат от пользователя {user_id}."
            )
        else:
            await context.bot.send_message(
                chat_id=psychologist_id,
                text="Пользователь уже находится в чате с другим психологом."
            )
    else:
        await context.bot.send_message(
            chat_id=psychologist_id,
            text="Вы не указали идентификатор пользователя для начала чата."
        )


async def handle_user_message(update: Update, context):
    user_id = update.effective_user.id

    if user_id in connections:
        psychologist_id = connections[user_id]
        message_text = update.message.text
        await context.bot.send_message(
            chat_id=psychologist_id,
            text=f"Пользователь {user_id} написал:\n\n{message_text}"
        )
        await context.bot.send_message(
            chat_id=user_id,
            text=f"Сообщение отправлено психологу: {message_text}"
        )
    else:
        await update.message.reply_text("Пожалуйста, начните чат с команды /chat.")


async def handle_psychologist_message(update: Update, context):
    psychologist_id = update.effective_user.id

    for user_id, connected_psychologist in connections.items():
        if connected_psychologist == psychologist_id:
            message_text = update.message.text
            await context.bot.send_message(
                chat_id=user_id,
                text=f"Психолог отвечает:\n\n{message_text}"
            )
            await context.bot.send_message(
                chat_id=psychologist_id,
                text=f"Вы отправили сообщение пользователю: {message_text}"
            )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await update.message.reply_text(f"Пока, {user.first_name}! Диалог завершен.")
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("learn", learn))
    application.add_handler(CommandHandler("diary", diary))
    application.add_handler(CommandHandler("crisis", crisis))
    application.add_handler(CommandHandler("tips", tips))
    application.add_handler(CommandHandler("groupsupport", group_support))
    application.add_handler(CommandHandler("progress", progress))
    application.add_handler(CommandHandler("express", express))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("accept", accept_chat))
    application.add_handler(CommandHandler("chat", chat))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(
        MessageHandler(filters.Chat(chat_id="461421538") & filters.TEXT, handle_psychologist_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
