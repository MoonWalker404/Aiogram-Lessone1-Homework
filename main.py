import asyncio
import logging
import aiohttp
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN, API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Список городов для случайного выбора
cities = [
    "Москва", "Санкт-Петербург", "Нью-Йорк", "Лондон", "Париж",
    "Берлин", "Токио", "Сидней", "Дубай", "Рим",
    "Торонто", "Мадрид", "Лос-Анджелес", "Бразилиа", "Пекин"
]

# Функция для получения данных о погоде
async def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Функция для отключения вебхуков
async def delete_webhook(token):
    url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            return await response.json()

# Основная функция
async def main():
    # Отключаем вебхуки
    await delete_webhook(TOKEN)

    dp = Dispatcher()
    bot = Bot(token=TOKEN)

    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.reply("Привет! Я бот, который предоставляет прогноз погоды. Используйте команду /weather для получения прогноза для случайного города.")

    @dp.message(Command("weather"))
    async def get_weather(message: types.Message):
        # Выбираем случайный город из списка
        city = random.choice(cities)
        data = await get_weather_data(city)

        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            response = (
                f"Погода в городе {city}:\n\n"
                f"- {weather.capitalize()}\n"
                f"- Температура: {temperature}°C\n"
                f"- Влажность: {humidity}%\n"
                f"- Скорость ветра: {wind_speed} м/с"
            )
            await message.reply(response)
        else:
            await message.reply("Не удалось получить прогноз погоды. Попробуйте позже.")

    @dp.message()
    async def echo_message(message: types.Message):
        await message.reply("Я не понимаю это сообщение. Используйте команду /weather для получения прогноза для случайного города.")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
