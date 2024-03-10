
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
critetia = {'name_bani': "А насколько обширен местный банный комплекс?",
            'vastness': "А как русская парная?",
            'rusbani': "Про сауну, что скажешь?",
            'sauna' : "Ну а хамам, хамам как?",
            'hamam' : "А с безопаснотью как, вещички есть куда спрятать?",
            'storage' : "Иновации есть или тут старая добрая классика?",
            'inovation' : "Еда как местная?",
            'food' : "С алкоголём, что пиво, водка есть?",
            'bar' : "Бани то красивые, есть чем полюбоваться?",
            'decor' : "Там нормально убираются или кругом срач?",
            'clean' : "Места для купания как? Есть где нормально отмокнуть?",
            'pool' : "С обслуживанием что?",
            'service' : "Что по ракам",
            'crayfish' : "Насколько эти бани аутентичны? Чувствуется банный колорит",
            'authenticity' : "А кроме самих бань, есть чем скрасить досуг?",
            'entertainment' : "Ну и самое главное, что по цене",
            'price' : "Фух, ну вроде всё спросил, внесу в базу"}
question_list = list(critetia)
count = 1


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

async def get_bani(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global test_bani
    global question_list
    global count
    global critetia
    crit = question_list[count - 1]
    question = critetia[crit]
    test_bani[crit] = update.message.text
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id = user_id, text= question)
    if(count != 17):
        count += 1
        return count
    count = 1
    return ConversationHandler.END



if __name__ == '__main__':

    # Непосредственное тело нашего бота, созданное с помощью метода ApplicationBuilder() из интегрированной библиотеки и нашего ключа
    application = ApplicationBuilder().token(parol).build()
    
    # Команда которая славливает команду /start и запускает соответствующий метод
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

# Для создание ветви необходима череда последовательных Хэндлеров, представляющая из себя словарь, тут мы его и создаём
    dict_question = {}
    for i in range(1, 18):
        dict_question[i] = [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bani)]

    # Ветвь тестовых вопросов
    handler = ConversationHandler(
        [CommandHandler("test", test)],
        dict_question,
        fallbacks=[]
    )
        
    application.add_handler(handler)

    # Наш обработчит inline кнопок (тут кнопки с callback = "test")
    application.add_handler(CallbackQueryHandler(start_test, "test"))
  
    # Команда, которая непосредственно запускает нашего бота и держит живым, нажав сочетание Ctrl + C остановит его
    application.run_polling()