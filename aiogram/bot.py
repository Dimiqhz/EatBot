import config
import functions

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.utils import executor

point = ''  # местоположение на карте (долгота и широта, разделенные ',')

print('Бот запущен.')
bot = Bot(token=config.token)
dp = Dispatcher(bot)

# функция обработки локации
# принимает местоположение пользователя и приводит к необходимому виду (долгота и широта, разделенные ',') для последующего отправления запроса в Яндекс
# вызывает функцию создания inline клавиатуры 
@dp.message_handler(content_types=['location'])
async def func_location(message: types.Message):
    global point
    point = f"{message.location.longitude},{message.location.latitude}"
    await functions.func_inline_button(bot, message.chat.id, functions.msg['start'])

# функция обработки команды /start
# создает клавиатуру с возможностью отправки местоположения
@dp.message_handler(commands=['start'])
async def func_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button = KeyboardButton(text='Отправить местоположение', request_location=True)
    keyboard.add(button)
    await bot.send_message(message.chat.id, functions.msg['loc'], reply_markup=keyboard)

# функция обработки inline кнопок
# запускает функцию поиска по организациям
# вызывает функцию создания inline клавиатуры
@dp.callback_query_handler(lambda call: True)
async def func_call(call: CallbackQuery):
    if point == '':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=functions.msg['loc'])
    elif call.data in {'Вкусно и Точка', 'KFC', 'Subway', 'Burger King'}:
        await functions.func_search_gis(bot, call, point)
    elif call.data == 'var':
        await functions.func_var(bot, call)

# функция обработки текста
# определяет геопозицию введенного пользователем адреса (в частности станции метро)
# вызывает функцию создания inline клавиатуры
@dp.message_handler(content_types=['text'])
async def func_text(message: types.Message):
    global point
    point = await functions.func_geo_gis(bot, message)
    await functions.func_inline_button(bot, message.chat.id, functions.msg['start'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
