
import logging
from typing import Optional, Union
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from telegram.ext._utils.types import FilterDataDict
from telegram.ext.filters import MessageFilter
from config import parol
from telegram.ext import ConversationHandler


# Наш логгер который записывает данные каждые 10 секунд
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Создаём словарь критериев:
test_bani = {}


# Метод команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Банная оценка", callback_data="like-trex")],
        [InlineKeyboardButton("Вывести Банную Базу", callback_data="like-trex")]
    ]
    await update.message.reply_text(text= "Здарова мужики, чего нужно", reply_markup= InlineKeyboardMarkup(keyboard))


# Тест
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Ну начнём опрос")
    await context.bot.send_message(chat_id = user_id, text= "И в каких банях были?")
    return 1

async def get_baniname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global test_bani
    test_bani['name_bani'] = update.message.text
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id = user_id, text= "А насколько обширен местный банный комплекс?")
    return ConversationHandler.END
    


if __name__ == '__main__':

    # Непосредственное тело нашего бота, созданное с помощью метода ApplicationBuilder() из интегрированной библиотеки и нашего ключа
    application = ApplicationBuilder().token(parol).build()
    
    # Команда которая славливает команду /start и запускает соответствующий метод
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Ветвь тестовых вопросов
    handler = ConversationHandler(
        [CommandHandler("test", test)],
        {
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_baniname)]
        },
        fallbacks=[]
    )
    application.add_handler(handler)
  
    # Команда, которая непосредственно запускает нашего бота и держит живым, нажав сочетание Ctrl + C остановит его
    application.run_polling()