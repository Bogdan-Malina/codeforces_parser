from parser.models import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData

load_dotenv()
API_TOKEN = os.getenv("TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

cb = CallbackData(
    'keyboard',
    'action',
    'page',
    'type_keyboard',
    'selected_tag',
    'selected_cmx'
)


def create_cb(
        action=' ',
        page=1,
        type_keyboard=1,
        selected_tag=1,
        selected_cmx=0
):
    callback = cb.new(
        action=action,
        page=page,
        type_keyboard=type_keyboard,
        selected_tag=selected_tag,
        selected_cmx=selected_cmx
    )

    return callback


async def create_tag_btn(
        page,
        keyboard_type,
        paginator_type,
        selected=0
):
    last_page = round(len(keyboard_type)/5)
    to_id = page*5
    from_id = to_id-5
    keyboard = types.InlineKeyboardMarkup()
    action = 'complexity'

    btn_arr = [
        types.InlineKeyboardButton(
            text='ВПЕРЕД',
            callback_data=create_cb(
                action='paginator',
                page=page + 1,
                type_keyboard=paginator_type,
                selected_tag=selected
            )
        ),
        types.InlineKeyboardButton(
            text='НАЗАД',
            callback_data=create_cb(
                action='paginator',
                page=page - 1,
                type_keyboard=paginator_type,
                selected_tag=selected
            )
        ),
        types.InlineKeyboardButton(
            text=f'{page}/{last_page}',
            callback_data='!'
        ),
        types.InlineKeyboardButton(
            text='ВЕРНУТЬСЯ К ТЭГАМ',
            callback_data=create_cb(
                action='paginator',
                page=1,
                type_keyboard=1,
                selected_tag=0
            )
        )
    ]

    if keyboard_type == Complexity:
        action = 'tasks'

    select = keyboard_type.select().where(
        (keyboard_type.id > from_id),
        (keyboard_type.id <= to_id)
    )

    for btn in select:
        keyboard.add(
            types.InlineKeyboardButton(
                text=f'{btn.name}',
                callback_data=create_cb(
                    action=action,
                    selected_tag=btn.id,
                    selected_cmx=selected
                )
            )
        )

    if page <= 1:
        keyboard.add(
            btn_arr[0],
            btn_arr[2]
        )
    elif page >= last_page:
        keyboard.add(
            btn_arr[1],
            btn_arr[2]
        )
    else:
        keyboard.add(
            btn_arr[1],
            btn_arr[0],
            btn_arr[2]
        )
    if keyboard_type == Complexity:
        keyboard.add(btn_arr[3])

    return keyboard


@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    await message.answer(
        '/meny',
    )


@dp.message_handler(commands=['meny'])
async def show_meny(message: types.Message) -> None:
    paginator_type = 1
    x = await message.answer('Выберите тэг:')
    keyboard = await create_tag_btn(1, Tag, paginator_type)
    await x.edit_reply_markup(keyboard)


@dp.callback_query_handler(cb.filter())
async def keyboard_callback(callback: types.CallbackQuery, callback_data: dict) -> None:
    if callback_data['action'] == 'paginator':
        selected = 0
        type_menu = Tag
        text = 'Выберите тэг:'
        msg = callback.message
        page = int(callback_data.get('page'))

        if callback_data.get('type_keyboard') == '2':
            type_menu = Complexity
            if callback_data.get('selected_tag') != '0':
                selected = callback_data.get('selected_tag')
                tag_name = Tag.get(Tag.id == selected).name
                text = f'Выбранный тэг - "{tag_name}"\n'
                text += 'Выберите сложность:'

        keyboard = await create_tag_btn(
            page,
            type_menu,
            callback_data['type_keyboard'],
            selected
        )
        if msg.text != text:
            await msg.edit_text(
                text
            )
        await msg.edit_reply_markup(keyboard)

    if callback_data['action'] == 'complexity':
        msg = callback.message
        paginator_type = 2
        keyboard = await create_tag_btn(
            1,
            Complexity,
            paginator_type,
            callback_data.get('selected_tag')
        )
        tag_name = Tag.get(
            Tag.id == callback_data.get('selected_tag')
        ).name
        text = f'Выбранный тэг - "{tag_name}"\nВыберите сложность:'
        await msg.edit_text(
            text
        )
        await msg.edit_reply_markup(keyboard)

    if callback_data['action'] == 'tasks':
        tag = Tag.get(Tag.id == callback_data.get('selected_cmx'))
        cmx = Complexity.get(Complexity.id == callback_data.get('selected_tag'))
        tasks = tag.tasks.where(Task.complexity == cmx).limit(10)
        text = ''
        for i in tasks:
            text += f'{i.task_id, i.name, i.complexity.name, i.solution}\n'
        if not text:
            text = 'Нет задач с выбранными параметрами'
        msg = callback.message
        keyboard = msg.reply_markup
        await msg.edit_text(
            text
        )
        await msg.edit_reply_markup(keyboard)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()

