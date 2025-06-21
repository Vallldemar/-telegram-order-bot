
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

API_TOKEN = '8168647860:AAEvORyhzYG9_rC8W2AoakF_9ust1UKy-NE'
ADMIN_ID = 439073803

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("Серия ЭКО"), KeyboardButton("Серия СТАНДАРТ"))
main_kb.add(KeyboardButton("Аксессуары"), KeyboardButton("Оформить заказ"), KeyboardButton("🗑 Очистить корзину"))

eco_kb = ReplyKeyboardMarkup(resize_keyboard=True)
eco_kb.add(KeyboardButton("ЭКО 200 Вт"), KeyboardButton("ЭКО 400 Вт"))
eco_kb.add(KeyboardButton("ЭКО 500 Вт"), KeyboardButton("ЭКО 620 Вт"))
eco_kb.add(KeyboardButton("ЭКО 800 Вт"))
eco_kb.add(KeyboardButton("⬅ Назад"))

standard_kb = ReplyKeyboardMarkup(resize_keyboard=True)
standard_kb.add(KeyboardButton("СТАНДАРТ 400 Вт"), KeyboardButton("СТАНДАРТ 500 Вт"))
standard_kb.add(KeyboardButton("СТАНДАРТ 620 Вт"), KeyboardButton("⬅ Назад"))

user_cart = {}
user_data = {}

@dp.callback_query_handler(Text(equals="reuse_data"))
async def reuse_delivery_data(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_cart[user_id] = user_data[user_id].copy()
    user_cart[user_id]["awaiting"] = "tk"
    tk_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    tk_kb.add(KeyboardButton("КИТ"), KeyboardButton("Деловые линии"), KeyboardButton("ПЭК"))
    await call.message.answer("Выберите транспортную компанию:", reply_markup=tk_kb)
    await call.answer()

@dp.callback_query_handler(Text(equals="reset_data"))
async def reset_delivery_data(call: types.CallbackQuery):
    user_cart[call.from_user.id] = {"items": [], "awaiting": "lastname"}
    await call.message.answer("Введите фамилию получателя:")
    await call.answer()

@dp.callback_query_handler(Text(equals="confirm"))
async def confirm_order(call: types.CallbackQuery):
    user_id = call.from_user.id
    items = user_cart.get(user_id, {}).get("items", [])
    if user_id in user_data:
        user_cart[user_id] = user_data[user_id].copy()
        user_cart[user_id]["items"] = items
        user_cart[user_id]["awaiting"] = "tk"
        tk_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        tk_kb.add(KeyboardButton("КИТ"), KeyboardButton("Деловые линии"), KeyboardButton("ПЭК"))
        await call.message.answer("Выберите транспортную компанию:", reply_markup=tk_kb)
    else:
        user_cart[user_id] = {"items": items, "awaiting": "lastname"}
        await call.message.answer("Введите фамилию получателя:")
    await call.answer()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_cart[user_id] = {"items": []}
    if user_id in user_data:
        reuse_text = (
            f"Использовать предыдущие данные доставки?\n\n"
            f"👤 {user_data[user_id]['lastname']} {user_data[user_id]['firstname']} {user_data[user_id]['middlename']}\n"
            f"🏙 {user_data[user_id]['city']}\n"
            f"📞 {user_data[user_id]['phone']}"
        )
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ Да, использовать", callback_data="reuse_data"),
            InlineKeyboardButton("✏ Ввести заново", callback_data="reset_data")
        )
        await message.answer(reuse_text, reply_markup=markup)
    else:
        await message.answer("Выберите категорию:", reply_markup=main_kb)

# Остальные хендлеры опущены для краткости...
