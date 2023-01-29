from aiogram import Bot, Dispatcher, executor, types
import pyqrcode
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import telebot 
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, CallbackQuery

CallbackContext is a convenience class used in the PTB framework to provide access to commonly used objects into your handler callbacks. For each update one instance of this class is built by the Dispatcher and passed to the handler callbacks as second argument.
bot = Bot(token = '5679962308:AAHUvmUUf5k5L9QW6g653Wt_1dCu02IVAY0')
dp = Dispatcher(bot, storage=MemoryStorage()) # Dispatcher is a class that work s with the updates through Handlers
# manages in-memory dictionaries that can be used to store bot/chat/user related data

button1 = KeyboardButton('Please share your contact number', request_contact = True)
button2 = KeyboardButton('Please share your current location', request_location = True)
keyboard1 = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button1).add(button2)

@dp.message_handler(commands=['name'])
async def greet(message: types.Message):
    user_first_name = str(message.chat.first_name) 
    await message.reply(message, f"Hey! {user_first_name}")

@dp.message_handler(commands = ['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Hello! I am FluoLingo", reply_markup = keyboard1)

@dp.message_handler(commands = ['info'])
async def info(message: types.Message):
    await message.reply("Say something to you: ", reply_markup = keyboard1)

class Form(StatesGroup):
    Q1 = State()  # First question
    Q2 = State()  # Second question
    Q3 = State()  # Third question

# Function to handle the user's message
@dp.message_handler(state='*', commands=['converse'])
async def process_start_command(message: Message):
    await bot.send_message(chat_id=message.chat.id, text="Hello, what is your name?")
    await Form.Q1.set()

 
# Function to handle the user's response to the first question
@dp.message_handler(state=Form.Q1)
async def process_name(message: Message, state: FSMContext):
    user_name = message.text
    await bot.send_message(chat_id=message.chat.id, text=f"Nice to meet you, {user_name}! How old are you?")
    await state.update_data(name=user_name)
    await Form.next()


# Function to handle the user's response to the second question
@dp.message_handler(state=Form.Q2)
async def process_age(message: Message, state: FSMContext):
    
    user_age = message.text
    await bot.send_message(chat_id=message.chat.id, text=f"Thank you for letting me know your age, your age is {user_age}! Can you please share your email-id?")
    await state.update_data(age=user_age)
    await Form.next()


# Function to handle the user's response to the third question
@dp.message_handler(state=Form.Q3)
async def process_email(message: Message, state: FSMContext):
    user_email = message.text
    await bot.send_message(chat_id=message.chat.id, text=f"Thanks for sharing your email, and your email-id is {user_email}.")
    await state.update_data(email=user_email)
    await state.finish()

executor.start_polling(dp)
