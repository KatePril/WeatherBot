from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp
from utils import save_users, load_users
from weather import get_weather


class RegForm(StatesGroup):
    name = State()
    city = State()

users = load_users()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if user_id not in [user['id'] for user in users]:
        await RegForm.name.set()
        await message.reply("Hi!\nI'm WeatherBot!\nHow shall I call you?")
        return
    
    await message.answer("Welcome to the chat") 

@dp.message_handler(state=RegForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await RegForm.next()
    await message.answer("Which city's weather would you like to know?")

@dp.message_handler(state=RegForm.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    
    data = await state.get_data()
      
    text = f"Check the data:\nName: {data['name']}\nCity: {data['city']}"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="Confirm"))
    markup.add(types.KeyboardButton(text="Try again"))
    await message.answer(text, reply_markup=markup)
    
@dp.message_handler(state=RegForm.city, text="Try again")
async def process_city_again(message: types.Message, state: FSMContext):
    await state.finish()
    await RegForm.name.set()
    await message.answer("How shall I call you?", reply_markup=types.ReplyKeyboardRemove())
    
@dp.message_handler(state=RegForm.city, text="Confirm")
async def process_city_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    users.append(dict(id=message.from_user.id, username=message.from_user.username, **data))
    save_users(users)
    await state.finish()
    await message.answer("Thank you, you are registrated now", reply_markup=types.ReplyKeyboardRemove())
    await send_welcome(message)
    
@dp.message_handler(state=RegForm.city, commands='get_weather')
async def send_weather(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(get_weather(data['name']))

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


