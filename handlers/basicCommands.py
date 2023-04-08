from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp
# from utils import save_users, load_users
from weather import get_weather


# class RegForm(StatesGroup):
#     name = State()

# users = load_users()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):    
    await message.answer("Which city's weather would you like to know?")
    
city = ''

@dp.message_handler(commands='get_weather')
async def send_weather(message: types.Message):
    global city
    await message.answer(get_weather(city))
    await message.answer('You can type another name of the city in the chat')

@dp.message_handler()
async def echo(message: types.Message):
    global city
    city = message.text
    await message.answer("Type '/get_weather' to get data or type another name of the city in the chat")


