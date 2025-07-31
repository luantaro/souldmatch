# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

waiting = []
active = {}

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("👋 Chào mừng đến với SoulMatch! Gõ /find để tìm người trò chuyện ẩn danh.")

@dp.message(Command("find"))
async def find_partner(message: types.Message):
    user_id = message.from_user.id
    if user_id in active:
        await message.answer("❗ Bạn đang trò chuyện rồi.")
        return

    if waiting and waiting[0] != user_id:
        partner_id = waiting.pop(0)
        active[user_id] = partner_id
        active[partner_id] = user_id

        await bot.send_message(user_id, "✅ Đã kết nối! Bắt đầu trò chuyện ẩn danh.")
        await bot.send_message(partner_id, "✅ Đã kết nối! Bắt đầu trò chuyện ẩn danh.")
    else:
        waiting.append(user_id)
        await message.answer("⏳ Đang chờ người khác vào trò chuyện...")

@dp.message(Command("stop"))
async def stop_chat(message: types.Message):
    user_id = message.from_user.id
    if user_id in active:
        partner_id = active.pop(user_id)
        active.pop(partner_id, None)

        await bot.send_message(user_id, "❌ Đã kết thúc trò chuyện.")
        await bot.send_message(partner_id, "❌ Đối phương đã rời cuộc trò chuyện.")
    elif user_id in waiting:
        waiting.remove(user_id)
        await message.answer("❌ Đã hủy tìm kiếm.")
    else:
        await message.answer("⚠️ Bạn chưa tham gia trò chuyện.")

@dp.message(F.text)
async def relay_message(message: types.Message):
    user_id = message.from_user.id
    if user_id in active:
        partner_id = active[user_id]
        await bot.send_message(partner_id, message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
