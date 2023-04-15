import logging

from aiogram import Bot, Dispatcher, executor, types
from configg import TOKEN
import requests
from bs4 import BeautifulSoup as BS

#BBBBBBBOOOOOOOOOOOOOOTTTTTTTTTTTT


                #ЗАПУСК БОТА
logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher(bot)

                #ПАРСИНГ
#ПАРСИНГ МЕНЮ
async def parsing_menu(menu_button):
    req = requests.get(url="https://yaponomaniya.com/")
    html = BS(req.content,'html.parser')

    for el in html.find_all("li", class_='categories-menu__item'):
        txt = el.find_all("div",class_="categories-menu__item-name")
        menu_button.append(txt[0].text)
    return (menu_button)
#ПАРСИНГ РОЛЛОВ
async def parsing_rull():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    req = requests.get(url="https://yaponomaniya.com/rolly", headers = headers)
    html = BS(req.content, 'html.parser')
    rull_button = []
    for el in html.find_all("li", class_="submenu-item"):
        txt = el.find_all("a", class_="submenu-link hover-link-target")
        if txt:
            rull_button.append(txt[0].text)
    return rull_button

#ПАРСИНГ ЕДЫ

async def parsing_eat(url):
    req = requests.get(url)
    soup = BS(req.content, 'html.parser')
    products = []
    for el in soup.find_all("li", class_='product-item set'):
        name = el.find("div", class_="text").get_text(strip=True)
        photo_url = el.find("img", class_="product-img")['src']
        description = el.find("div", class_="product-desc").get_text(strip=True)
        price = el.find("span", class_="price new h3").get_text(strip=True).replace('\xa0', "")
        products.append({'name': name, 'photo_url': photo_url, 'description': description, 'price': price})
    return products

#ТОВАРЫ С КНОПКАМИ
async def handle_menu_callback(call: types.CallbackQuery, URL: str):
    products = await parsing_eat(URL)
    markup = types.InlineKeyboardMarkup(row_width=1)
    korzina = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='korzina')
    per_korzina = types.InlineKeyboardButton(text='Перейти в корзину', callback_data='per_korzina')
    markup.add(korzina, per_korzina)
    for product in products:
        message = f'Name: {product["name"]}\n'
        message += f'Description: {product["description"]}\n'
        message += f'Price: {product["price"]}\n'
        photo_url = product['photo_url']
        full_url = "https://yaponomaniya.com/" + photo_url
        await bot.send_photo(chat_id=call.from_user.id, photo=full_url,
                             caption=f"{product['name']}\n\n {'Описание: ' + product['description']}\n\n{product['price']}",
                             reply_markup=markup)


   #СТАРТ БОТА
@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):

    markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    button_zakaz = types.KeyboardButton(text="Совершить заказ")
    markup.add(button_zakaz)
    await message.answer("Приветствуем вас в Япономании.", reply_markup=markup)

            # КНОПКИ ЗАКАЗА
@dp.message_handler(lambda message: message.text == "Совершить заказ")
async def with_puree(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    menu_button = await parsing_menu([])
    button = [
        [types.InlineKeyboardButton(text=text.strip(), callback_data=text.strip())] for text in menu_button
    ]

    markup.add(*[button for sublist in button for button in sublist])
    await message.answer("что вы хотите заказать?", reply_markup=markup)



#--------------------------------------------ОБРАБОТКА КНОПОК МЕНЮ-------------------------------------------------------------------------------


@dp.callback_query_handler(text="Сеты")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/assorty')

@dp.callback_query_handler(text="Комбо")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/kombo')

@dp.callback_query_handler(text="Пиццы")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/pitstsy')

@dp.callback_query_handler(text="Горячее")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/goryachee')

@dp.callback_query_handler(text="Ланч-меню")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/lanch-menyu')

@dp.callback_query_handler(text="Салаты и фри")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/salaty-i-fri')

@dp.callback_query_handler(text="Тортильи и бургеры")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/tortilji')

@dp.callback_query_handler(text="Суши и гунканы")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/sushi_i_-karai')

@dp.callback_query_handler(text="Десерты и напитки")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/deserty-i-napitki')

@dp.callback_query_handler(text="Добавки")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/dobavki')

#++++++++++++++++++++++++Роллы++++++++++++++++++++++++++++++++++=
@dp.callback_query_handler(text="Роллы")
async def menu(call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=1)
    rull_button = await parsing_rull()
    button = [
        [types.InlineKeyboardButton(text=text.strip(), callback_data=text.strip())] for text in rull_button
    ]
    markup.add(*[button for sublist in button for button in sublist])
    await call.message.answer("Выберите роллы которые вы хотите", reply_markup=markup)

@dp.callback_query_handler(text="В темпуре")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/rolly/gorjachie_rolly')

@dp.callback_query_handler(text="Запеченные")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/rolly/zapechenye_roly')

@dp.callback_query_handler(text="Классические")
async def menu(call: types.CallbackQuery):
    await andle_menu_callback(call, 'https://yaponomaniya.com/rolly/srednye_rolly')

@dp.callback_query_handler(text="Малые")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/rolly/malie_rolly')

@dp.callback_query_handler(text="Премиальные")
async def menu(call: types.CallbackQuery):
    await handle_menu_callback(call, 'https://yaponomaniya.com/rolly/premialnye')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
