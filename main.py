import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiohttp

API_URL = "https://<ТВОЙ-АДРЕС-НА-CYCLIC>/results/"  # ← сюда вставь адрес своего API
BOT_TOKEN = "твой_токен_бота"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Кнопочная клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("🚀 Сделать замер"))
keyboard.add(KeyboardButton("📊 Мои замеры"))
keyboard.add(KeyboardButton("🔄 Обновить"))

@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для проверки скорости интернета 📡\n\nВыбери действие на клавиатуре ниже:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "📊 Мои замеры")
async def get_results(message: types.Message):
    user_id = str(message.from_user.id)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL + user_id) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    text = "📊 Твои последние замеры:\n\n"
                    for result in data:
                        text += (f"🔻 Download: {result['download_speed']} Mbps\n"
                                 f"🔺 Upload: {result['upload_speed']} Mbps\n"
                                 f"📶 Ping: {result['ping']} ms\n"
                                 f"🕒 {result['timestamp']}\n"
                                 f"--------------------\n")
                    await message.answer(text)
                else:
                    await message.answer("Ошибка при получении данных с сервера 😢")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@dp.message(lambda message: message.text == "🔄 Обновить")
async def refresh_results(message: types.Message):
    await get_results(message)

@dp.message(lambda message: message.text == "🚀 Сделать замер")
async def start_speedtest(message: types.Message):
    await message.answer("🚀 Запускаю замер скорости...\nОжидаю данные от приложения 📡")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())