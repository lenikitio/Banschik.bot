
import logging
from typing import Optional, Union
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from telegram.ext._utils.types import FilterDataDict
from telegram.ext.filters import MessageFilter
from config import parol
from telegram.ext import ConversationHandler, CallbackQueryHandler


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
        [InlineKeyboardButton("Банная оценка", callback_data="test")],
        [InlineKeyboardButton("Вывести Банную Базу", callback_data="base")]
    ]
    await update.message.reply_text(text= "Здарова мужики, чего нужно", reply_markup= InlineKeyboardMarkup(keyboard))

async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Убираем кнопки
    await update.callback_query.message.edit_reply_markup(None)

    # Меняем текст сообщения
    text_сhat = "Запрос принят, в личной беседе о бане и поговорим"
    await update.callback_query.edit_message_text(text_сhat)
    # Отправляем сообщение в личный чат
    text_id = "Напиши команду /test и начнём"
    await context.bot.send_message(update.effective_user.id, text_id)
    
    
# Тест
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
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
            1 : [MessageHandler(filters.TEXT & ~filters.COMMAND, get_baniname)]
        },
        fallbacks=[]
    )

    application.add_handler(handler)

    # Наш обработчит inline кнопок (тут кнопки с callback = "test")
    application.add_handler(CallbackQueryHandler(start_test, "test"))
  
    # Команда, которая непосредственно запускает нашего бота и держит живым, нажав сочетание Ctrl + C остановит его
    application.run_polling()