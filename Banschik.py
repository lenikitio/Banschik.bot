
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from telegram.ext.filters import MessageFilter
from config import parol


# Наш логгер который записывает данные каждые 10 секунд
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Метод команды старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup([["Сходили в баню, нужно отценить"], ["А в каких банях мы были?"]])
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Здарова мужики, чего нужно", reply_markup= markup)

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Переходи в соответствующую комнату, там тебя и опросим")
    await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id= 1529, text="В какие бани ходили?")

# Создаём класс фильтр для того, чтобы наш бот реагировал на определённую фразу
class FilterStartBanschik(MessageFilter):
    def filter(self, message):
        return 'Ей банщик' in message.text

class FilterTestBanschik(MessageFilter):
    def filter(self, message):
        return 'Сходили в баню, нужно отценить' in message.text





if __name__ == '__main__':
    # Непосредственное тело нашего бота, созданное с помощью метода ApplicationBuilder() из интегрированной библиотеки и нашего ключа
    application = ApplicationBuilder().token(parol).build()
    
    startBanschik = FilterStartBanschik()
    test_banschik = FilterTestBanschik()

    # Команда которая славливает команду /start и запускает соответствующий метод
    start_handler = MessageHandler(startBanschik, start)
    application.add_handler(start_handler)

    test_handler = MessageHandler(test_banschik, test)
    application.add_handler(test_handler)


    
    # Команда, которая непосредственно запускает нашего бота и держит живым, нажав сочетание Ctrl + C остановит его
    application.run_polling()