from parser.models import *
import parser.main_parser as test

import schedule
import logging
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '5439256003:AAF4RZzN4NWCUGQX_NBPPPub4bPPYM-G3Ho'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def create_keyboard():
    btn = Tag.select().execute()
    keyboard = types.InlineKeyboardMarkup()
    for i in btn:
        keyboard.add(
            types.InlineKeyboardButton(
                text=i.name,
                callback_data=f'{i.id}'
            )
        )

        @dp.callback_query_handler(text=f'{i.id}')
        async def send_random_value(call: types.CallbackQuery):
            query = Tag.get(Tag.id == int(call.data))
            msg = ''
            for i in query.tasks.order_by(Task.complexity):
                msg += f'{i.id} - {i.name} - f{i.complexity} - f{i.solution}\n'

            await call.message.answer(msg)
    return keyboard


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    keyboard = create_keyboard()
    await message.reply(
        "Выбери тэг",
        reply_markup=keyboard
    )


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


def main():
    schedule.every(5).seconds.do(test.parser)
    schedule.run_pending()
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
