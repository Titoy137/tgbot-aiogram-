async def on_startup(_):
    await db_start()


storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot,
                storage=storage)


class ProfileStatesGroup(StatesGroup):

    name = State()
    age = State()
    description = State()


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/создать_профиль'))

    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/отмена'))

    return kb


@dp.message_handler(commands=['отмена'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply('Вы прервали создание профиля!',
                        reply_markup=get_kb())


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('Welcome! So as to create profile - type /создать_профиль',
                         reply_markup=get_kb())

    await create_profile(user_id=message.from_user.id)


@dp.message_handler(commands=['создать_профиль'])
async def cmd_create(message: types.Message) -> None:
    await message.reply("Давай создадим тебе профиль!\nВеди свое имя!",
                        reply_markup=get_cancel_kb(
                        ))
    await ProfileStatesGroup.name.set()



@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Сколько тебе лет?')
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 110, state=ProfileStatesGroup.age)
async def check_age(message: types.Message):
    await message.reply('Введите реальный возраст!')


@dp.message_handler(state=ProfileStatesGroup.age)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply('А теперь расскажи немного о себе!')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.description)
async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_photo(chat_id=message.from_user.id,
                             caption=f"{data['name']}, {data['age']}\n{data['description']}")

    await edit_profile(state, user_id=message.from_user.id)
    await message.reply('Ваша акнета успешно создана!')
    await state.finish()