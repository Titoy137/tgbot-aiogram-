from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

bot = Bot(token="5858878196:AAEnQS-LrX0m6OVEL85vSSnkhEvfg9Z7gnU")
dp = Dispatcher(bot)

#---------------------------------------генерация промокода-----------------------------------------------
def get_promo_code(num_chars):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code

#---------------------------------------------лабиринт-------------------------------------------------------
get_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

item1 = types.KeyboardButton('Прямо')
item2 = types.KeyboardButton('Налево')

get_kb.add(item1, item2)

@dp.message_handler(commands=['start'])
async def startap(message: types.Message):
    await message.reply(f'Ты в начале лабиринта\n Куда пойдешь?', reply_markup=get_kb)

@dp.message_handler(text="Прямо")
async def get_text_messages(message: types.Message):
    markupInl = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Поверну налево')
    item2 = types.KeyboardButton('Поверну направо')

    markupInl.add(item1, item2)

    await message.reply('Ты подошёл к очередной развилке\nЧто решишь сделать?', reply_markup=markupInl)

@dp.message_handler(text="Налево")
async def get_text_messages(message: types.Message):
    markupInl = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Вернуться')
    markupInl.add(item1)
    await message.reply('Ты зашёл в тупик!', reply_markup=markupInl)

@dp.message_handler(text="Поверну налево")
async def get_text_messages(message: types.Message):
    markupInl = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Назад на главную')
    markupInl.add(item1)
    await message.reply(f'Ты прошёл лабиринт, молодец!\nПолучай промокод! {get_promo_code(num_chars=10)}', reply_markup=markupInl)

@dp.message_handler(text="Поверну направо")
async def get_text_messages(message: types.Message):
    markupInl = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Назад')
    markupInl.add(item1)
    await message.reply('Ты зашёл в тупик!', reply_markup=markupInl)

# ----------------------------------------кнопки возврата---------------------------------------------------------------
@dp.message_handler(text="Вернуться")
async def get_text_messages(message: types.Message):
    markupInl = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Прямо')
    item2 = types.KeyboardButton('Налево')
    markupInl.add(item1, item2)
    await message.reply('Ты вернулся обратно к развилке', reply_markup=markupInl)

@dp.message_handler(text="Назад")
async def get_text_messages(message: types.Message):
    markupInl = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поверну налево')
    item2 = types.KeyboardButton('Поверну направо')
    markupInl.add(item1, item2)
    await message.reply('Ты вернулся обратно к развилке', reply_markup=markupInl)

if __name__ == '__main__':
    executor.start_polling(dp)