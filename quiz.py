import qs, db, re
import asyncio, logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
# ----------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)

API_TOKEN = '7650355573:AAEQGqLVivjumgyniXjhiNFfYLpcYbYkGHM'
API_TOKEN = 'YOUR_API_KEY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
# ----------------------------------------------------------------------------
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Begin the quiz'))
    builder.add(types.KeyboardButton(text='See results'))
    await message.answer(text=f"Hey! Do you want to do a <b>Which Harry Potter character are you most like</b> quiz?", parse_mode='HTML', 
                         reply_markup=builder.as_markup(resize_keyboard=True))
# ----------------------------------------------------------------------------
@dp.message(F.text=='Begin the quiz')
@dp.message(Command('quiz'))
async def cmd_quiz(message: types.Message):
    await message.answer('OK. Let\'s begin!')
    await new_quiz(message)
# ----------------------------------------------------------------------------
@dp.message(F.text=='See results')
@dp.message(Command('results'))
async def cmd_results(message: types.Message):
    msg = ''
    results = await db.get_results()

    if len(results) == 0:
        msg = f"You are the first!"
    else:
        for result in results:
            msg = msg + f"\nID: {result[0]} — {result[1]}"
        
    await message.answer(text=msg, parse_mode='HTML')
# ----------------------------------------------------------------------------
async def new_quiz(message):
    user_id = message.from_user.id

    await db.update_quiz_index(user_id, 0, '')
    await get_question(message, user_id)
# ----------------------------------------------------------------------------
async def get_question(message, user_id):
    current_question_index = await db.get_quiz_index(user_id)
    opts = qs.quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts)

    await message.answer(f"{qs.quiz_data[current_question_index]['question']}", reply_markup=kb)
# ----------------------------------------------------------------------------
def generate_options_keyboard(answer_options):
    builder = InlineKeyboardBuilder()

    for i in range(len(answer_options)):
        option = str([answer_options[i], i])
        builder.add(types.InlineKeyboardButton(text=answer_options[i], callback_data=option))
    builder.adjust(1)

    return builder.as_markup()
# ----------------------------------------------------------------------------
@dp.callback_query()
async def chosen(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                                message_id=callback.message.message_id,
                                                reply_markup=None)
    
    current_question_index = await db.get_quiz_index(callback.from_user.id)
    current_question_index += 1
    unpacked = re.sub(r'([\]\[\'\"])+', '', callback.data).split(',')

    await db.update_quiz_index(callback.from_user.id, current_question_index, unpacked[1].strip(' '))
    await callback.message.answer(text=f"<b>{unpacked[0]}</b>", parse_mode='HTML')

    if current_question_index < len(qs.quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        verdict = await db.get_verdict(callback.from_user.id)
        await callback.message.answer(f"You are most like {str(verdict)}")
# ----------------------------------------------------------------------------
async def main():
    await db.create_table()
    await dp.start_polling(bot)
# ----------------------------------------------------------------------------
if __name__ == '__main__':
    asyncio.run(main())