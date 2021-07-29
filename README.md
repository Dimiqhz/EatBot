# Элементарный Telegram-бот, выполняющий основные функции
## Бот для поиска ближайших ресторанов быстрого питания

Программа производит поиск ближайших заведений по отправленному пользователем местоположению или названию станции метро в СПб. Также она предоставляет выбор между _четырьмя_ ресторанами:
 + McDonald’s
 + KFC
 + Subway
 + Burger King
 
Бот присылает местоположение ближайших заведений с помощью точек на картах. Пользователь может выбрать ресторан, наиболее подходящий его требованиям.  

Отправление локаций пользователю оптимизировано и содержит мало сообщений: отправляется одна локация и предоставляется вариант выбора другой, либо же выбора другого ресторана. 

[Видео с функционированием бота](https://drive.google.com/file/d/1--etGkIuulyfVxT6oECJTEflRvLrKDIb/view?usp=sharing)

## Основные моменты при реализации

Бот написан на языке python 3, с помощью библиотеки pyTelegramBotAPI (документация [Telegram Bot API](https://core.telegram.org/bots/api)). Для реализации бота создано три файла.

В файле _bot_eat.py_ расположены основные функции бота, реагирующие на отклики пользователя. 

Файл _functions.py_ содержит реализации функций, необходимых для корректной работы программы. В нем находятся как функции для реализации работы с картами, так и функции вывода текста и кнопок. 

API-ключи, как и token бота, были помещены в файл _config.py_. Для запуска программы необходимо добавить индивидуальные данные в этот файл.

## Реализация поиска заведений и геокодера 

Работа с картами была реализована с помощью сервиса _2gis_. Он не требует подключения нескольких ключей для выполнения разных действий. Для реализации были использованы
+ _**Geocoder API**_
    - Для определения координат станций метро, введенных пользователем. 
    - Использовано в функции func_geo_gis.
    - [Документация Geocoder API для 2gis](https://docs.2gis.com/ru/api/search/geocoder/overview).
    - [Альтернатива при использовании сервисов Яндекс: API Геокодера](https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/about.html).
+ _**Places API**_ 
    - Для нахождения ближайших заведений на карте по координатам в определенном радиусе. 
    - Использовано в функции func_search_gis.
    - [Документация Places API для 2gis](https://docs.2gis.com/ru/api/search/places/overview).
    - [Альтернатива при использовании сервисов Яндекс: API поиска по организациям](https://yandex.ru/dev/maps/geosearch/doc/concepts/about.html).
