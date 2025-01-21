from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import logging
import crud_functions


logging.basicConfig(level=logging.INFO)
api = 'мой токен'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

'''инициализация базы данных'''
crud_functions.initiate_db()

'''основная клавиатура кнопок'''
btkey = ReplyKeyboardMarkup(
	keyboard = [
		[KeyboardButton(text = 'Рассчитать'),
		KeyboardButton(text = 'Информация')],
		[KeyboardButton(text = 'Купить витамины')]
	], resize_keyboard=True
)

'''инлайн клавиатура расчёта калорий'''
inkey = InlineKeyboardMarkup(resize_keyboard=True)
calori = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
formulas = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
inkey.add(calori)
inkey.add(formulas)

'''инлайн клавиатура каталога'''
catalokey = InlineKeyboardMarkup(
	inline_keyboard = [
		[InlineKeyboardButton(text = 'Магний', callback_data = 'product_buying'),   		
		InlineKeyboardButton(text = 'Железо', callback_data ='product_buying' ),		    
		InlineKeyboardButton(text = 'Витамин С', callback_data = 'product_buying'),	
		InlineKeyboardButton(text = 'Витамин D', callback_data = 'product_buying')]
	], resize_keyboard=True
)

'''класс для хранения введённых параметров расчета калорий'''
class UserState(StatesGroup):
	age = State()
	growth = State()
	weight = State()
		
'''про калории'''			
@dp.message_handler(text='Рассчитать' )
async def main_menu(message):
	await message.answer('Выберите опцию:', reply_markup = inkey)
	
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
	await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
	await call.answer()	
	
@dp.callback_query_handler(text='calories')
async def set_age(call):
	await call.message.answer('Введите свой возраст:')
	await UserState.age.set()
	
@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
	await state.update_data(age= message.text)
	print('Запущен алгоритм рассчета калорий')
	await message.answer('Введите свой рост:')
	await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
	await state.update_data(growth= message.text)
	await message.answer('Введите свой вес:')
	await UserState.weight.set()
	
'''расчет калорий на основании введенных параметров'''
@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
	await state.update_data(weight= message.text)
	data = await state.get_data()
	age = int(data['age'])
	growth = int(data['growth'])
	weight = int(data['weight'])
	calories  = 10 * weight + 6.25 * growth - 5 * age - 161
	await message.answer(f'Ваша норма калорий: {calories} ккал')
	await state.finish()
	

'''блок продажи'''
@dp.message_handler(text='Купить витамины')
async def get_buying_list(message):
    print(f'{message.from_user.username} выбирает витамины')
    products = crud_functions.get_all_products()

    for product in products:
        await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        with open(f'{product[1]}.jpg', 'rb') as img:
            await message.answer_photo(img)

    await message.answer('Выберите продукт для покупки:', reply_markup=catalokey)

    '''презентация товаров без БД'''
    # names = ['Магний', 'Железо', 'Витамин С', 'Витамин D']
    # img_names = ['magnesium.jpg', 'ferrum.jpg', 'vitaminC.jpg', 'vitaminD.jpg' ]
    # descriptions = ['Важен для здоровья сердца, костей, нервной системы, сна, мышечной функции и общего метаболизма',
    #  'Необходимо для транспортировки кислорода в крови, поддержания энергии, иммунной функции и когнитивного здоровья',
    #  'Поддерживает иммунную систему, способствует заживлению ран, улучшает всасывание железа и действует как антиоксидант',
    #  'Важен для здоровья костей, иммунной системы, регуляции настроения и общего метаболизма']
    # prices = 100


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
	await call.message.answer('Вы успешно приобрели продукт!')
	await call.answer()
       	

'''начало работы с ботом'''
@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Бот запущен')
    await message.answer(f'Привет, {message.from_user.username}! Я бот помогающий твоему здоровью.', reply_markup = btkey)
    
@dp.message_handler(text='Информация')
async def info_message(message):
    print('Запрошена информация о боте')
    with open('Welcome.jpg', 'rb') as img:
    	await message.answer_photo(img, 'Этот бот рассчитывает норму калорий для девушек и продаёт витамины =)')

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение')
        

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
