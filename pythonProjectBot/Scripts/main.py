from create_prifill import db_start, create_profile, edit_profile
from configg import TOKEN, PAYMENTS_PROVIDER_TOKEN
from create_comment import create_comment, db_start_com, edit_comment
from create_korzina import db_start_krz, create_korzina, edit_korzina
from parsing import parsing_eat, handle_menu_callback, parsing_eat, parsing_rull, parsing_menu
from labitinth import get_promo_code

import openai
import sqlite3 as sq
from aiogram import types, Dispatcher, executor, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def on_startup(_):
    await db_start()
    await db_start_com()
    await db_start_krz()

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
db = sq.connect('new.db')

class ProfileStatesGroup(StatesGroup):

    photo = State()
    name = State()
    age = State()
    description = State()

    commentariy = State()

    zakaz = State()
    kolvo = State()



#Менюшка снопок
get_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

item1 = types.KeyboardButton('Совершить заказ')
item2 = types.KeyboardButton('Сыграть в игру')
item3 = types.KeyboardButton('Профиль')
item4 = types.KeyboardButton('Поговорить с интернет умом')
get_kb.add(item1, item2, item3, item4)



PRICE = types.LabeledPrice(label='Настоящая Машина Времени', amount=420000)
@dp.message_handler(commands=['terms'])
async def process_terms_command(message: types.Message):
    await message.reply(message['terms'], reply=False)




@dp.message_handler(commands=['buy'])
async def process_buy_command(message: types.Message):
    if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'pre_buy_demo_alert')
    await bot.send_invoice(
        message.chat.id,
        title='tm_title',
        description='tm_description',
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency='rub',
        photo_height=512,  # !=0/None, иначе изображение не покажется
        photo_width=512,
        photo_size=512,
        is_flexible=False,  # True если конечная цена зависит от способа доставки
        prices=[PRICE],
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use'
    )

@dp.message_handler(text="Вернуться в меню")
async def with_puree(message: types.Message):
    await message.reply('Вы вернулись в меню',reply_markup = get_kb)

#Пишем отклин на комманду старт
@dp.message_handler(commands=['start'])
async def startap(message: types.Message):

    user_name = message.from_user.first_name

    await bot.send_sticker(message.from_user.id, sticker= "CAACAgIAAxkBAAIZPWPI8f7TBht-Ny6p6VBAkNV-XwgNAAIaAAOQ_ZoVj-YTCjJewM8tBA" )
    await message.reply(f'<em>Привет,{user_name}\nДобро пожаловать в бота Япономании</em>', parse_mode='HTML', reply_markup = get_kb)


@dp.message_handler(text="Сыграть в игру")
async def with_puree(message: types.Message):

    gget_kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    item1 = types.KeyboardButton('Прямо')
    item2 = types.KeyboardButton('Налево')
    iten = types.KeyboardButton('Вернуться в меню')
    gget_kb.add(item1, item2, iten)

    await message.reply('Ты в начале лабиринта!\nКуда ты пойдешь?', reply_markup=gget_kb)
    @dp.message_handler(text="Прямо")
    async def get_text_messages(message: types.Message):
        mmarkupInl = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        item1 = types.KeyboardButton('Поверну налево')
        item2 = types.KeyboardButton('Поверну направо')
        iten = types.KeyboardButton('Вернуться в меню')
        mmarkupInl.add(item1, item2,iten)

        await message.reply('Ты подошёл к очередной развилке\nЧто решишь сделать?', reply_markup=mmarkupInl)

@dp.message_handler(text="Налево")
async def get_text_messages(message: types.Message):
    mmarkupInl = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton('Вернуться')
    iten = types.KeyboardButton('Вернуться в меню')
    mmarkupInl.add(item1, iten)
    await message.reply('Ты зашёл в тупик!', reply_markup=mmarkupInl)

@dp.message_handler(text="Поверну налево")
async def get_text_messages(message: types.Message):
    mmarkupInl = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    iten = types.KeyboardButton('Вернуться в меню')
    mmarkupInl.add(iten)
    await message.reply(f'Ты прошёл лабиринт, молодец!\nПолучай промокод на скидку 10%! {get_promo_code(num_chars=10)}\nОбязательно его используй в течение недели, иначе он сгорит.',
                        reply_markup=mmarkupInl)

@dp.message_handler(text="Поверну направо")
async def get_text_messages(message: types.Message):
    mmarkupInl = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton('Назад')
    iten = types.KeyboardButton('Вернуться в меню')
    mmarkupInl.add(item1,iten)
    await message.reply('Ты зашёл в тупик!', reply_markup=mmarkupInl)

# ----------------------------------------кнопки возврата---------------------------------------------------------------
@dp.message_handler(text="Вернуться")
async def get_text_messages(message: types.Message):
    mmarkupInl = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('Прямо')
    item2 = types.KeyboardButton('Налево')
    iten = types.KeyboardButton('Вернуться в меню')
    mmarkupInl.add(item1, item2, iten)
    await message.reply('Ты вернулся обратно к развилке', reply_markup=mmarkupInl)

@dp.message_handler(text="Назад")
async def get_text_messages(message: types.Message):
    mmarkupInl = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('Поверну налево')
    item2 = types.KeyboardButton('Поверну направо')
    iten = types.KeyboardButton('Вернуться в меню')
    mmarkupInl.add(item1, item2, iten)
    await message.reply('Ты вернулся обратно к развилке', reply_markup=mmarkupInl)


#Пишем отклик на кнопку меню
@dp.message_handler(text="Совершить заказ")
async def with_puree(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    menu_button = await parsing_menu([])
    button = [
        [types.InlineKeyboardButton(text=text.strip(), callback_data=text.strip())] for text in menu_button
    ]

    markup.add(*[button for sublist in button for button in sublist])
    await message.answer("Что вы хотите заказать?", reply_markup=markup)



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
        await handle_menu_callback(call, 'https://yaponomaniya.com/rolly/srednye_rolly')

    @dp.callback_query_handler(text="Малые")
    async def menu(call: types.CallbackQuery):
        await handle_menu_callback(call, 'https://yaponomaniya.com/rolly/malie_rolly')

    @dp.callback_query_handler(text="Премиальные")
    async def menu(call: types.CallbackQuery):
        await handle_menu_callback(call, 'https://yaponomaniya.com/rolly/premialnye')





@dp.message_handler(text="Профиль")
async def get_text_messages(message: types.Message):

    markupInl = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Сделать профиль')
    item2 = types.KeyboardButton('Написать отзыв')

    markupInl.add(item2, item1)

    await message.reply('Выбери что ты хочешь сделать: ',reply_markup=markupInl)

@dp.message_handler(text="Сделать профиль")
async def cmd_create(message: types.Message) -> None:

        # Проверяем есть ли профиль уже в базе
        user_id = message.from_user.id
        with sq.connect('new.db') as connection:

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM myprofile WHERE user_id = ? ", (user_id,))
            data = cursor.fetchone()

            if data is None:

                await bot.send_message(message.from_user.id,"Давай создадим тебе профиль!\nВведи свое имя!", reply_markup=get_cancel_kb())
                await create_profile(user_id=message.from_user.id)
                await ProfileStatesGroup.name.set()

                @dp.message_handler(state=ProfileStatesGroup.name)
                async def load_name(message: types.Message, state: FSMContext) -> None:

                    async with state.proxy() as data:
                        data['name'] = message.text

                    await bot.send_message(message.from_user.id, 'Сколько тебе лет?')
                    await ProfileStatesGroup.next()

                @dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 110,
                                    state=ProfileStatesGroup.age)
                async def check_age(message: types.Message):

                    await bot.send_message(message.from_user.id, 'Введите реальный возраст!')

                @dp.message_handler(state=ProfileStatesGroup.age)
                async def load_name(message: types.Message, state: FSMContext) -> None:

                    async with state.proxy() as data:
                        data['age'] = message.text

                    await bot.send_message(message.from_user.id, 'А теперь расскажи немного о себе!')
                    await ProfileStatesGroup.next()

                @dp.message_handler(state=ProfileStatesGroup.description)
                async def load_desc(message: types.Message, state: FSMContext) -> None:

                    async with state.proxy() as data:

                        data['description'] = message.text
                        data['photo'] = "https://yt3.ggpht.com/a/AGF-l7875YxhMiA2466YQoQmRMMvf3rBtOPZ-D89fQ=s900-c-k-c0xffffffff-no-rj-mo"

                        await bot.send_photo(chat_id=message.from_user.id,
                                                photo=data['photo'],
                                                caption=f"{data['name']}, {data['age']}\n{data['description']}")

                    await edit_profile(state, user_id=message.from_user.id)
                    await message.answer('Ваша акнета успешно создана!', reply_markup=get_kb)
                    await state.finish()

            else:

                await message.answer('Аккаунт уже создан', reply_markup=get_kb)


# @dp.callback_query_handler(text="Добавить в корзину")
# async def send_kz(call: types.CallbackQuery):
#
#     await bot.send_message(call.message.from_user.id, "Подтвердите",
#                            reply_markup=get_cancel_kb())
#     await create_korzina(user_id=call.message.from_user.id)
#     await ProfileStatesGroup.zakaz.set()
#
#     @dp.message_handler(state=ProfileStatesGroup.zakaz)
#     async def load_name(message: types.Message, state: FSMContext) -> None:
#         async with state.proxy() as data:
#             parsing_eat(data['zaraz'] = product['name'])
#
#         await bot.send_message(call.message.chat.id, 'Введи количество')
#         await ProfileStatesGroup.next()
#
#         @dp.message_handler(state=ProfileStatesGroup.kolvo)
#         async def load_desc(message: types.Message, state: FSMContext) -> None:
#             async with state.proxy() as data:
#                 data['kolvo'] = message.text
#                 data['photo'] = "https://yt3.ggpht.com/a/AGF-l7875YxhMiA2466YQoQmRMMvf3rBtOPZ-D89fQ=s900-c-k-c0xffffffff-no-rj-mo"
#
#                 await bot.send_photo(chat_id=message.from_user.id,
#                                      photo=data['photo'],
#                                      caption=f"{data['kolvo']}")
#
#             await edit_profile(state, user_id=message.from_user.id)
#             await message.answer('ТОвар добавлен в корзину!', reply_markup=get_kb)
#             await state.finish()




@dp.callback_query_handler(text="Перейти в корзину")
async def send_kz(call: types.CallbackQuery):
    pass

@dp.message_handler(commands=['отмена заказа', 'emptythetrash'], state='*')
async def korzin_cancel(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    with sq.connect('new.db') as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM mykorzin WHERE user_id = ?", (user_id,))

    if state is None:
        return

    await state.finish()
    await message.reply('Успешно выполненно!',
                        reply_markup=get_kb)


def get_cancel_kb() -> ReplyKeyboardMarkup:

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/отмена_создания'))

    return kb


def get_cancel_kb2() -> ReplyKeyboardMarkup:

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/отмена'))

@dp.message_handler(commands=['отмена', 'deletecom'], state='*')
async def comment_cancel(message: types.Message, state: FSMContext):

        user_id = message.from_user.id
        with sq.connect('new.db') as connection:

            cursor = connection.cursor()
            cursor.execute("DELETE FROM mypcomment WHERE user_id = ?", (user_id,))

        if state is None:

            return

        await state.finish()
        await message.reply('Успешно выполненно!',
                            reply_markup=get_kb)


@dp.message_handler(commands=['отмена_создания', 'deleteprof'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    with sq.connect('new.db') as connection:

        cursor = connection.cursor()
        cursor.execute("DELETE FROM myprofile WHERE user_id = ?", (user_id,))

    if state is None:

        return

    await state.finish()
    await message.reply('Успешно выполненно!', reply_markup=get_kb)


#Пишем отклик на кнопку отзыв
@dp.message_handler(text="Написать отзыв")
async def cm_create(message: types.Message) -> None:

    user_id = message.from_user.id
    with sq.connect('new.db') as connection:

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM mypcomment WHERE user_id = ? ", (user_id,))
        data = cursor.fetchone()

        if data is None:

            await message.reply("Отлично!\nВведи комментарий!",
                                    reply_markup=get_cancel_kb2())
            await create_comment(user_id=message.from_user.id)
            await ProfileStatesGroup.commentariy.set()

            @dp.message_handler(state=ProfileStatesGroup.commentariy)
            async def load_com(message: types.Message, state: FSMContext) -> None:

                async with state.proxy() as data:

                    data['commentariy'] = message.text
                    data['photo'] = "https://yt3.ggpht.com/a/AGF-l7875YxhMiA2466YQoQmRMMvf3rBtOPZ-D89fQ=s900-c-k-c0xffffffff-no-rj-mo"
                    await bot.send_photo(chat_id=message.chat.id,
                                            photo=data['photo'],
                                            caption=f"\n{data['commentariy']}")

                await edit_comment(state, user_id=message.from_user.id)
                await message.answer('Ваша комментарий добавлен!', reply_markup = get_kb)
                await state.finish()

        else:

            await message.answer('Лимит комментариев исчерпан', reply_markup = get_kb)

openai.api_key = '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'


#Разговор с нейросетью
@dp.message_handler(text="Поговорить с интернет умом")
async def test(message):
    await message.answer('Начинай диалог', reply_markup=get_kb)
    @dp.message_handler(content_types=['text'])
    async def echo(message: types.Message) -> None:

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"""
                        Я очень умный бот, отвечающий на вопросы. Если ты задашь мне вопрос, основанный на истине,
                        Я дам вам ответ.
                      Если вы зададите мне вопрос, который является ерундой, обманом или не имеет четкого ответа,
                        Я отвечу \"Unknown\".\n\n
                        Q: Какова продолжительность жизни человека в США?\n
                        A: Средняя продолжительность жизни человека в США составляет 78 лет.\n\n
                        Q: Кто был президентом США в 1955 году?\n
                        A: Дуайт Д. Эйзенхауэр был президентом США в 1955 году.\n\n
                        Q: К какой партии он принадлежал?\n
                        A: Он принадлежал к Республиканской партии.\n\n
                        Q: Чему равен квадратный корень из банана?\n
                        A: Unknown\n\n
                        Q: Как работает телескоп?\n
                        A: В телескопах используются линзы или зеркала, чтобы сфокусировать свет и сделать объекты ближе.\n\n
                        Q: Как играть в футбол?\n
                        A: В футбол играют ногами.\n\n
                        Q: Где проходили Олимпийские игры 1992 года?\n
                        A: Олимпийские игры 1992 года проходили в Барселоне, Испания.\n\n
                        Q: Какой год сейчас?\n
                        A: Сейчас 2023 год\n\n
                        Q: Что ты умеешь?\n
                        A: Если ты задашь мне вопрос, основанный на истине, Я дам вам ответ.\n\n
                        Q: {message.text}\n
                        A:""",
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        await message.answer(response["choices"][0]["text"])

#Запускаем
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
