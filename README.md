# Элементарный Telegram-бот, выполняющий основные функции
## Бот для поиска ближайших ресторанов быстрого питания

Программа производит поиск ближайших заведений по отправленному пользователем местоположению или названию станции метро в СПб. Также она предоставляет выбор между четырьмя ресторанами:
+ McDonald’s
+ KFC
+ Subway
+ Burger King

Бот присылает местоположение ближайших заведений с помощью точек на картах. Пользователь может выбрать ресторан, наиболее подходящий его требованиям.

## Реализация поиска заведений и геокодера 

Работа с картами была реализована двумя способами с помощью двух сервисов - _Яндекс API_ и _2gis_. API-ключи, как и token бота, были помещены в файл config.py. Оба варианта реализации бота являются взаимозаменяемыми.  

Для реализации работы с _**Яндекс**_ были подключены два API-ключа для использования 
+ JavaScript API и HTTP Геокодер  
    - Для определения координат станций метро, введенных пользователем. 
    - Использовано в функции func_geo_yandex.
+ API Поиска по организациям  
    - Для нахождения ближайших заведений на карте по координатам в определенном радиусе. 
    - Использовано в функции func_search_yandex.

Также была реализована работа с _**2gis**_, он не требует подключения нескольких ключей для разных действий. Для реализации были использованы
+ Geocoder API
    - Для определения координат станций метро, введенных пользователем. 
    - Использовано в функции func_geo_gis.
+ Places API
    - Для нахождения ближайших заведений на карте по координатам в определенном радиусе. 
    - Использовано в функции func_search_gis.
