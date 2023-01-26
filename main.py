import sqlite3

from aiogram import Dispatcher, executor, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage # локальное хранилищк в котором будем сохранять состояния
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboard import *
from config import TOKEN_API
from aiogram.dispatcher.filters import Text, Command
from text import HELP_COMMAND, DICE_RULES, CUPS_START, SLOT_START
import asyncio
from random import randrange
import sqlite_db
from sqlite_db import *


storage = MemoryStorage()
bot = Bot(token=TOKEN_API,
          parse_mode='HTML')
dp = Dispatcher(bot,
                storage=storage)



class ProfileStatesGroup(StatesGroup):

    name = State()
    balance = State()


async def on_startup(_):
    await sqlite_db.db_start()
    print('Connect to bd is complited')


# async def show_all_balance(callback: types.CallbackQuery, profile: list) -> None:
#     for balances in profile:
#         await bot.send_photo(chat_id=callback.message.chat.id,
#                              caption=f'<b>{balances[1]}</b> {balances[0]}',
#                              parse_mode='HTML',
#                              reply_markup=get_cancel_kb())


@dp.message_handler(Text(equals='Cancel 🚫'), state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.reply('You interrupted creating a profile',
                        reply_markup=get_sign_kb())


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='Welcome to our casino bot!',
                         reply_markup=get_sign_kb())
    await create_profile(user_id=message.from_user.id)


# @dp.message_handler(Text(equals='Help 🆘'))
# async def help_command(message: types.Message):
#     await message.answer(text=HELP_COMMAND,
#                          parse_mode='HTML')
#

@dp.message_handler(Text(equals='Tap to sign up ☑️'))
async def cmd_profile(message: types.Message) -> None:
    await message.answer('Let\'s create your profile! To begin with, send me your name!',
                         reply_markup=get_cancel_kb())
    await ProfileStatesGroup.name.set()


@dp.message_handler(lambda message: not message.text or len(message.text) < 2 or len(message.text) > 15,
                    state=ProfileStatesGroup.name)
async def check_name(message: types.Message):
    await message.reply('Name can consist only 2-15 symbols')

#
# @dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 500,
#                     state=ProfileStatesGroup.balance)
# async def check_balance(message: types.Message):
#     await message.reply('You can top up only 500 points or less')

# content_types=['name'],


@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('How much money do you want on your balance?')
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 500,
                    state=ProfileStatesGroup.balance)
async def check_balance(message: types.Message):
    await message.reply('You can top up only 500 points or less')


@dp.message_handler(state=ProfileStatesGroup.balance)
async def make_balance(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['balance'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"<b>Name:</b>  {data['name']}\n<b>Balance:</b>  {data['balance']} points.",
                               parse_mode='HTML')

    await edit_profile(state, user_id=message.from_user.id)
    await message.reply('Congratulations! You\'ve done your profile.\n You can play games.',
                        reply_markup=kb_main)
    await state.finish()


@dp.message_handler(Text(equals='Help 🆘'))
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND,
                         parse_mode='HTML')


@dp.message_handler(Text(equals='Games 🕹'))
async def games_command(message: types.Message):
    await message.answer(text='Now you can choose the game!',
                         reply_markup=kb_games)


@dp.message_handler(Text(equals='Profile 👤'))
async def main(message: types.Message):
    con = sqlite3.connect('info.db')
    cur = con.cursor()
    a = cur.execute(f'SELECT balance FROM profile WHERE user_id = {message.from_user.id}').fetchall()[0][0]
    b = cur.execute(f'SELECT name FROM profile WHERE user_id = {message.from_user.id}').fetchall()[0][0]
    await bot.send_message(message.from_user.id,
                           text=f'<b>Name:</b> {b}\n\n<b>Balance:</b> {a} points.',
                           reply_markup=kb_main)


#
# @dp.callback_query_handler(text='select_profile')
# async def cb_get_balance_info(callback: types.CallbackQuery):
#     profile_info = await sqlite_db.select_profile()
#
#     await callback.message.delete()
#     await show_all_balance(callback, profile_info)
#     await callback.answer()  # чтоб не было тайминга на кнопке
#

@dp.message_handler(Text(equals='Exit ⛔️'))
async def stop_dice(message: types.Message):
    await message.answer(text='You\'re in main menu',
                         reply_markup=kb_main)


@dp.message_handler(Text(equals='Dice 🎲'))
async def dice_game(message: types.Message):
    await message.answer(text=DICE_RULES,
                         reply_markup=kb_dice,
                         parse_mode='HTML')

    @dp.message_handler(Text(equals='Roll the 🎲'))
    async def dice_spin(message: types.Message):
        await change_balance_game(user_id=message.from_user.id)
        await bot.send_message(message.from_user.id, 'It\'s your turn')
        user_data = await bot.send_dice(message.from_user.id)
        user_data = user_data['dice']['value']
        await asyncio.sleep(5)

        await bot.send_message(message.from_user.id, 'It\'s bot\'s turn')
        bot_data = await bot.send_dice(message.from_user.id)
        bot_data = bot_data['dice']['value']
        await asyncio.sleep(5)

        if bot_data > user_data:
            await bot.send_message(message.from_user.id,
                                   f'You lost the game and 2 points ☠️\nTry again!')
        elif bot_data < user_data:
            await change_balance_win(user_id=message.from_user.id)
            await bot.send_message(message.from_user.id, f'You won 4 points! 🏆')
        else:
            await change_balance_draw(user_id=message.from_user.id)
            await bot.send_message(message.from_user.id, f'It\'s a draw 🤝\nTry again!')

    @dp.message_handler(Text(equals='Stop game ⛔'))
    async def stop_dice(message: types.Message):
        await message.answer(text='You\'re in game menu',
                             reply_markup=kb_games)


@dp.message_handler(Text(equals='Magic cups ✨'))
async def cups_game(message: types.Message):
    await message.answer(text=CUPS_START,
                         reply_markup=kb_cups_in,
                         parse_mode="HTML")

    @dp.message_handler(Text(equals='Mix 🔄'))
    async def cups_game(message: types.Message):
        await bot.send_animation(chat_id=message.from_user.id,
                                 animation='CgACAgIAAxkBAAOeY6yrXpGtI6ELIj1OIAvz26VT0fwAAq87AAIOO2hJCQxwhwfCJ18sBA')
        # await bot.delete_message(message.from_user.id, message_id_to_del)
        await message.answer(text="Choose cup 1, 2, 3",
                             reply_markup=kb_cups_game)

        @dp.message_handler(Text(equals=['1', '2', '3']))
        async def number_equals(message: types.Message):
            bot_datas = randrange(1, 4)
            if message.text == str(bot_datas):
                await change_balance_game_wincups(user_id=message.from_user.id)
                await bot.send_message(chat_id=message.from_user.id, text='🎉')
                await bot.send_message(chat_id=message.from_user.id, text='You guessed right cup!',
                                       reply_markup=kb_cups_in)

            else:
                await change_balance_game_cups(user_id=message.from_user.id)
                await bot.send_message(chat_id=message.from_user.id, text='🚫')
                await bot.send_message(chat_id=message.from_user.id, text='Yoo didn\'t guess, try again!',
                                       reply_markup=kb_cups_in)

    # @dp.message_handler(content_types=ContentType.ANIMATION)
    # async def send_animation_file_id(message: types.Message):
    #     await message.answer(text='Send video')
    #     await message.reply(message.animation.file_id)
    @dp.message_handler(Text(equals='Stop game ⛔'))
    async def stop_dice(message: types.Message):
        await message.answer(text='You\'re in game menu',
                             reply_markup=kb_games)


@dp.message_handler(Text(equals='Slots 🎰'))
async def cups_game(message: types.Message):
    await message.answer(text=SLOT_START,
                         reply_markup=kb_slot,
                         parse_mode="HTML")

    @dp.message_handler(Text(equals='Spin ⭕️'))
    async def spin_command(message: types.Message):
        await change_balance_game(user_id=message.from_user.id)
        slots = await bot.send_dice(chat_id=message.from_user.id, emoji='🎰')
        slots = slots['dice']['value']
        await asyncio.sleep(2)

        if slots == 1:
            await slot_win_10points(user_id=message.from_user.id)
            await message.answer("You won 10 points!")
        elif slots == 64:
            await slot_win_100points(user_id=message.from_user.id)
            await message.answer("🎉")
            await message.answer("YOU WON 100 POINTS! 💰")
        elif slots == 43:
            await slot_win_50points(user_id=message.from_user.id)
            await message.answer("🍋🍋🍋\n\nYou won 50 points!")
        elif slots == 22:
            await slot_win_25points(user_id=message.from_user.id)
            await message.answer("🫐🫐🫐\n\nYou won 25 points!")
        else:
            await message.answer("You didn't win 😢\n\nTry again!")

    @dp.message_handler(Text(equals='Stop game ⛔'))
    async def stop_dice(message: types.Message):
        await message.answer(text='You\'re in game menu',
                             reply_markup=kb_games)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
