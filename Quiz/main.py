import json
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = ""

with open("question.json", "r", encoding="utf-8") as file:
    questions_data = json.load(file)


def get_keyboard(buttons: list):
    kb = ReplyKeyboardBuilder()
    for button in buttons:
        kb.add(KeyboardButton(text=button))
    return kb.as_markup()




bot = Bot(BOT_TOKEN)
dp = Dispatcher()

class Answers(StatesGroup):
    wait_for_answer_1 = State()
    wait_for_answer_2 = State()
    wait_for_answer_3 = State()

@dp.message(Answers.wait_for_answer_3 and F.text == 'Exit')
async def exit(message: types.Message, state: FSMContext):
    await state.clear()

@dp.message(F.text == '/start')
async def cmd_start(message: types.Message, state: FSMContext):
    question = questions_data['question_1']
    await message.answer(question['text'], reply_markup=get_keyboard(question['answers']))
    await state.set_state(Answers.wait_for_answer_1)


@dp.message(Answers.wait_for_answer_1)
async def step_2(message: types.Message, state: FSMContext):
    await state.update_data({'question_1': message.text})
    question = questions_data['question_2']
    await message.answer(question['text'], reply_markup=get_keyboard(question['answers']))
    await state.set_state(Answers.wait_for_answer_2)

@dp.message(Answers.wait_for_answer_2)
async def step_3(message: types.Message, state: FSMContext):
    await state.update_data({'question_2': message.text})
    question = questions_data['question_3']
    await message.answer(question['text'], reply_markup=get_keyboard(question['answers']))
    await state.set_state(Answers.wait_for_answer_3)


@dp.message(Answers.wait_for_answer_3)
async def step_4(message: types.Message, state: FSMContext):

    data = await state.get_data()
    data['question_3'] = message.text
    print(data)
    for question, answer in data.items():
        current_question_data = questions_data[question]
        if answer == str(current_question_data['right_answer']):
            await message.answer(f'ваш ответ на вопрос {current_question_data["text"]} правильный')
        else:
            await message.answer(f'ваш ответ на вопрос {current_question_data["text"]} НЕПРАВИЛЬНЫЙ')

    await state.clear()



if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))