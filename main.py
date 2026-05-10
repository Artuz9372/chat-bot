import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = "8352637347:AAE3hICTFuCIrRnud2LKkqMcE79tgLVFpRg"


bot = Bot(token=TOKEN)
dp = Dispatcher()

# 👥 очередь поиска
waiting_users = []

# 💬 активные чаты
active_chats = {}


# ---------------- START ----------------
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "💬 Анонимный чат знакомств\n\n"
        "/find — найти собеседника\n/stop — выйти из чата"
    )


# ---------------- FIND ----------------
@dp.message(Command("find"))
async def find(message: Message):

    uid = message.from_user.id

    # уже в чате
    if uid in active_chats:
        await message.answer("❌ ты уже в чате. /stop чтобы выйти")
        return

    # если есть кто-то в очереди → матч
    if waiting_users:

        partner = waiting_users.pop(0)

        active_chats[uid] = partner
        active_chats[partner] = uid

        await bot.send_message(uid, "💘 собеседник найден! пиши сообщение")
        await bot.send_message(partner, "💘 собеседник найден! пиши сообщение")

    else:
        waiting_users.append(uid)
        await message.answer("⏳ ищем собеседника...")


# ---------------- STOP ----------------
@dp.message(Command("stop"))
async def stop(message: Message):

    uid = message.from_user.id

    # выйти из чата
    if uid in active_chats:

        partner = active_chats.pop(uid)
        active_chats.pop(partner, None)

        await message.answer("❌ чат завершён")
        await bot.send_message(partner, "❌ собеседник вышел из чата")

        return

    # выйти из очереди
    if uid in waiting_users:
        waiting_users.remove(uid)
        await message.answer("❌ поиск остановлен")
        return

    await message.answer("ты не в чате")


# ---------------- MESSAGE RELAY ----------------
@dp.message()
async def chat(message: Message):

    uid = message.from_user.id

    if uid not in active_chats:
        return

    partner = active_chats[uid]

    await bot.send_message(
        partner,
        f"💬 собеседник:\n{message.text or 'медиа'}"
    )


# ---------------- RUN ----------------
async def main():
    await dp.start_polling(bot)


if name == "main":
    asyncio.run(main())