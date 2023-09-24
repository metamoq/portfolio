import logging
import telegram
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from telegram import ReplyKeyboardMarkup

connections = {}
# Установите токен бота, полученный от BotFather
TOKEN = '6380285902:AAEGqAQNbpEw0UgnBLDfmG-IlV1RPSgxQ6I'
bot = telegram.Bot(token=TOKEN)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Создаем клавиатуру с кнопками для всех команд и их пояснениями
    commands_keyboard = [
        ["/learn - Образовательные материалы"],
        ["/diary - Ведение дневника настроения"],
        ["/crisis - Контакты экстренной помощи"],
        ["/tips - Советы и упражнения"],
        ["/groupsupport - Групповая поддержка"],
        ["/progress - Отслеживание прогресса"],
        ["/express - Творческое выражение эмоций"],
        ["/chat - Начать анонимный чат с психологом"],
        ["/cancel - Завершить чат"],
    ]

    reply_markup = ReplyKeyboardMarkup(commands_keyboard, resize_keyboard=True)

    await update.message.reply_text("Привет! Я бот для поддержки психологического благополучия. "
                                  "Вот список доступных команд и их описаний:", reply_markup=reply_markup)

    reply_markup = ReplyKeyboardMarkup(commands_keyboard, resize_keyboard=True)

# Обработчик команды /learn
async def learn(update, context):
    # Добавьте здесь код для предоставления образовательных материалов
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Здесь вы можете получить образовательные материалы "
                                        "о психологическом благополучии и стратегиях управления эмоциями.")

# Обработчик команды /diary
async def diary(update, context):
    # Добавьте здесь код для ведения дневника настроения
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Вы можете вести дневник настроения, записывая свои эмоции и состояние. "
                                        "Просто отправьте сообщение с вашей записью.")

# Обработчик команды /crisis
async def crisis(update, context):
    # Добавьте здесь код для предоставления контактов экстренной психологической помощи
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Если у вас кризисная ситуация, пожалуйста, обратитесь за помощью по следующим контактам:\n"
                                        "1.[Кирилл - Вор Эмоций] - Телефон: +375292369785\n"
                                        "2.[Telegram] - https://t.me/squidtwister\n"
                                   )


# Обработчик команды /tips
async def tips(update, context):
    # Добавьте здесь код для предоставления советов и упражнений
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Вот несколько советов и упражнений, которые могут вам помочь управлять стрессом:\n"
                                        "1. Проводите время на свежем воздухе и занимайтесь физической активностью.\n"
                                        "2. Практикуйте глубокое дыхание и медитацию.\n"
                                        "3. Ведите дневник настроения и обращайте внимание на свои эмоции.\n"
                                        "4. Поговорите с близкими людьми о своих чувствах и проблемах.\n"
                                        "5. Попробуйте творческие методы выражения, такие как рисование или музыка.")

# Обработчик команды /groupsupport
async def group_support(update, context):
    # Добавьте здесь код для создания группового чата для поддержки
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Вы можете создать групповой чат для поддержки с другими пользователями, которые также ищут поддержку.")

# Обработчик команды /progress
async def progress(update, context):
    # Добавьте здесь код для отслеживания прогресса пользователя
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Вы можете отслеживать свой психологический прогресс и получать аналитику о вашем состоянии.")

# Обработчик команды /express
async def express(update, context):
    # Добавьте здесь код для творческого выражения эмоций
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Творческое выражение эмоций может быть замечательным способом обработки эмоций. Попробуйте рисовать, писать стихи, играть на музыкальных инструментах или заниматься чем-то другим, что вас вдохновляет.")

# Обработчик команды /help
async def help_command(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Я здесь, чтобы помочь вам управлять стрессом, тревожностью и депрессией. "
                                        "Вот что я могу сделать:\n\n"
                                        "/chat - Начать анонимный чат с психологом\n"
                                        "/learn - Получить образовательные материалы\n"
                                        "/diary - Вести дневник настроения\n"
                                        "/crisis - Получить контакты экстренной помощи\n"
                                        "/tips - Получить советы и упражнения\n"
                                        "/groupsupport - Создать групповой чат для поддержки\n"
                                        "/progress - Просмотреть свой прогресс\n"
                                        "/express - Творчески выразить свои эмоции")


psychologist_ids = ['461421538']  # Замените на реальные идентификаторы ваших психологов

# Создайте словарь для отслеживания активных чатов
active_chats = {}

# Создайте словарь для отслеживания активных чатов между пользователями и психологами
psychologist_connections = {}
connections = {}
psychologist_requests = {}
# ...

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Проверяем, что пользователь не уже находится в анонимном чате
    if user_id not in connections:
        # Ищем доступных психологов (те, которые не связаны ни с одним пользователем)
        available_psychologists = set(psychologist_ids) - set(connections.values())

        if available_psychologists:
            # Выбираем первого доступного психолога
            psychologist_id = available_psychologists.pop()

            # Отправляем запрос психологу
            await context.bot.send_message(
                chat_id=psychologist_id,
                text=f"Пользователь {user_id} хочет начать анонимный чат. Примите запрос, введя /accept {user_id}"
            )

            # Добавляем пользователя в словарь connections
            connections[user_id] = psychologist_id

            await update.message.reply_text("Ожидайте, пока психолог примет ваш запрос.")
        else:
            await update.message.reply_text("Извините, в данный момент нет доступных психологов. Попробуйте позже.")
    else:
        await update.message.reply_text("Вы уже находитесь в анонимном чате с психологом.")




async def accept_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    psychologist_id = update.effective_user.id

    # Получаем идентификатор пользователя из аргументов команды
    if context.args:
        user_id = context.args[0]

        # Проверяем, что соединение не установлено
        if user_id not in active_chats:
            # Создаем чат между психологом и пользователем
            active_chats[user_id] = psychologist_id
            connections[user_id] = psychologist_id

            await context.bot.send_message(
                chat_id=user_id,
                text="Ваш запрос на чат был принят. Вы начали анонимный чат с психологом. Пожалуйста, напишите ваш вопрос или проблему."
            )
            await context.bot.send_message(
                chat_id=psychologist_id,
                text=f"Вы приняли запрос на чат с пользователем {user_id}. Пожалуйста, напишите ваш ответ."
            )
        else:
            await context.bot.send_message(
                chat_id=psychologist_id,
                text="Пользователь уже находится в анонимном чате с другим психологом."
            )
    else:
        await context.bot.send_message(
            chat_id=psychologist_id,
            text="Вы не указали идентификатор пользователя для начала чата."
        )





# Обработчик текстовых сообщений от пользователей
async def handle_user_message(update: Update, context):
    user_id = update.effective_user.id

    if user_id in connections:
        psychologist_id = connections[user_id]
        message_text = update.message.text
        await context.bot.send_message(
            chat_id=psychologist_id,
            text=f"Пользователь {user_id} написал:\n\n{message_text}"
        )
    else:
        await update.message.reply_text("Пожалуйста, начните чат с команды /chat.")


async def handle_psychologist_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    psychologist_id = update.effective_user.id
    message_text = update.message.text

    for user_id, connected_psychologist in connections.items():
        if connected_psychologist == psychologist_id:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"Психолог отвечает:\n\n{message_text}"
            )
            break


# Обработчики команды /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Пока, {user.first_name}! Диалог завершен.")
    return ConversationHandler.END

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("learn", learn))
    application.add_handler(CommandHandler("diary", diary))
    application.add_handler(CommandHandler("crisis", crisis))
    application.add_handler(CommandHandler("tips", tips))
    application.add_handler(CommandHandler("groupsupport", group_support))
    application.add_handler(CommandHandler("progress", progress))
    application.add_handler(CommandHandler("express", express))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("chat", chat))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("chat", chat))
    application.add_handler(CommandHandler("accept", accept_chat))
    application.add_handler(MessageHandler(filters.USER and filters.TEXT, handle_user_message))
    application.add_handler(
        MessageHandler(filters.Chat(chat_id="461421538") & filters.TEXT, handle_psychologist_message))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
