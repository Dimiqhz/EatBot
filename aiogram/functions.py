import config
import functions

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.utils import executor

result = ''  # результат, приходящий через get-запрос, приведенный к словарю
len = 0  # количество найденных заведений
cnt = 0  # номер найденного заведения
msg = {  # сообщение, которые выводятся пользователю
    'start': 'Тут можно перекусить.. Что выберешь?)',
    'loc': 'Покажи на карте, где ты находишься\n\nНу а если ты в СПб, можешь ввести ближайшую станцию метро..',
    'call': 'Оо.. Есть еще места, где можно перекусить, можешь выбрать'
}

bot = Bot(token=config.token)
dp = Dispatcher(bot)


# функция определения геопозиции введенного пользователем адреса (в частности станции метро) с помощью 2gis
# выполнение запроса к Geocoder API 2gis (get-запрос: gis_geo) с ключом API_key_gis
async def func_geo_gis(message: types.Message) -> str:
    query = 'СПб метро ' + message.text
    r = await bot.session.get(config.gis_geo, params={
        'q': query,
        'key': config.API_key_gis,
        'fields': 'items.point'
    })
    result_data = await r.json()
    point = f"{result_data['result']['items'][0]['point']['lon']},{result_data['result']['items'][0]['point']['lat']}"
    return point


# функция поиска по местам с помощью 2gis
# работает с помощью библиотеки requests, запросы отправляются и принимаются согласно документации API поиска по организациям
# выполнение запроса Places API 2gis (get-запрос: gis_search) с ключом API_key_gis
async def func_search_gis(call: CallbackQuery, point: str) -> None:
    r = await bot.session.get(config.gis_search, params={
        'q': call.data,
        'key': config.API_key_gis,
        'point': point,
        'type': 'branch',
        'fields': 'items.point,items.schedule',
        'radius': '1000'
    })
    global result, cnt
    result = await r.json()
    cnt = 0
    await func_output_gis(call)


# функция вывода на результатов поиска мест при реализации с помощью 2gis
async def func_output_gis(call: CallbackQuery) -> None:
    if result['meta']['code'] == 200:
        global len
        len = result['result']['total']
        if len == 1:
            text1 = 'Я нашел ' + call.data + '! Но только ' + str(len) + ' ресторан'
        elif 1 < len < 5:
            text1 = 'Я нашел ' + call.data + '! Даже ' + str(len) + ' ресторана'
        else:
            text1 = 'Я нашел ' + call.data + '! Целых ' + str(len) + ' ресторанов'
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=text1)

        keyboard = types.InlineKeyboardMarkup()
        if len > 1:
            button = types.InlineKeyboardButton(text='Хочу другое место', callback_data='var')
            keyboard.add(button)
        button1 = types.InlineKeyboardButton(text='Вкусно и Точка', callback_data='Вкусно и Точка')
        button2 = types.InlineKeyboardButton(text='KFC', callback_data='KFC')
        keyboard.add(button1, button2)
        button3 = types.InlineKeyboardButton(text='Subway', callback_data='Subway')
        button4 = types.InlineKeyboardButton(text='Burger King', callback_data='Burger King')
        keyboard.add(button3, button4)
        await bot.send_venue(chat_id=call.message.chat.id,
                             latitude=result['result']['items'][0]['point']['lat'],
                             longitude=result['result']['items'][0]['point']['lon'],
                             title=result['result']['items'][0]['name'],
                             address=result['result']['items'][0]['address_name'],
                             reply_markup=keyboard)
    else:
        text1 = 'Ресторанов ' + call.data + ' рядом нет..('
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=text1)
        await func_inline_button(call.message.chat.id, msg['call'])


# функция смены найденной локации на другую
# происходит перебот элементов в списке с счетчиком cnt
async def func_var(call: CallbackQuery) -> None:
    global cnt
    if cnt < len - 1:
        cnt = cnt + 1
    elif cnt == len - 1:
        cnt = 0
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Выбрать другое место', callback_data='var')
    keyboard.add(button)
    button1 = types.InlineKeyboardButton(text='Вкусно и Точка', callback_data='Вкусно и Точка')
    button2 = types.InlineKeyboardButton(text='KFC', callback_data='KFC')
    keyboard.add(button1, button2)
    button3 = types.InlineKeyboardButton(text='Subway', callback_data='Subway')
    button4 = types.InlineKeyboardButton(text='Burger King', callback_data='Burger King')
    keyboard.add(button3, button4)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_venue(chat_id=call.message.chat.id,
                         latitude=result['result']['items'][cnt]['point']['lat'],
                         longitude=result['result']['items'][cnt]['point']['lon'],
                         title=result['result']['items'][cnt]['name'],
                         address=result['result']['items'][cnt]['address_name'],
                         reply_markup=keyboard)


# функция создания inline клавиатуры
async def func_inline_button(c_id: int, text: str) -> None:
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    button1 = types.InlineKeyboardButton(text='Вкусно и Точка', callback_data='Вкусно и Точка')
    button2 = types.InlineKeyboardButton(text='KFC', callback_data='KFC')
    keyboard.add(button1, button2)
    button3 = types.InlineKeyboardButton(text='Subway', callback_data='Subway')
    button4 = types.InlineKeyboardButton(text='Burger King', callback_data='Burger King')
    keyboard.add(button3, button4)
    await bot.send_message(c_id, text, reply_markup=keyboard)


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message) -> None:
    global point
    point = f"{message.location.longitude},{message.location.latitude}"
    await func_inline_button(message.chat.id, msg['start'])


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message) -> None:
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button = KeyboardButton(text='Отправить местоположение', request_location=True)
    keyboard.add(button)
    await bot.send_message(message.chat.id, msg['loc'], reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True)
async def handle_callback(call: CallbackQuery) -> None:
    if point == '':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=msg['loc'])
    elif call.data in {'Вкусно и Точка', 'KFC', 'Subway', 'Burger King'}:
        await func_search_gis(call, point)
    elif call.data == 'var':
        await func_var(call)


@dp.message_handler(content_types=['text'])
async def handle_text(message: types.Message) -> None:
    global point
    point = await func_geo_gis(message)
    await func_inline_button(message.chat.id, msg['start'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
