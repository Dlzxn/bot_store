from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter, CommandObject
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
from dotenv import load_dotenv
import os
import sqlite3
import telebot
from aiogram.types import FSInputFile
from defs.defd import ref_prov, db_table_val, from_bd, zamena_para, progr, del_otn
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram import types
import base64
import logging.config
import logging
from log_cfg.def_log import start_log, user_new
from log_cfg.logging_conf import logging_config
from admin import adm_rout
from keyboard.keyb import keyboard_menu, keyboard_menu_true, keyboard_menu_return, keyboard_menu_otn


router = Router()


@router.message(Command(commands=['chmok']))
async def process_button_chmok(callback: CallbackQuery, bot: Bot):
    progr(callback.from_user.id, from_bd(4, callback.from_user.id), 5)
    await callback.answer(f'Вы поцеловали свою половинку❤️\n\n'
                          f'Прогресс отношений: +5'
                          )
    await bot.send_message(from_bd(4, callback.from_user.id), "❤️Ваш партнер вас поцеловал❤️")


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'Вас приветствует бот бот для парочек!\n'
                         f'Здесь вы можете настраивать и развивать свои отношения\n'
                         f'Для взаимодействия отправьте /start\n'
                         )
    print(message)

@router.message(CommandStart)
async def start_cm(message: types.Message):
    if ref_prov(message.from_user.id)==False:
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username
        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
        user_new(us_name, us_id)
    if from_bd(4, message.from_user.id)==None:
        await message.answer_photo(photo=FSInputFile('image/menu.jpg', filename='кру'),
                        caption=f'Приветствую тебя в боте любви!\n'
                        f'Для построения отношений выберите "Создать отношения"',
                        reply_markup=keyboard_menu
                        )
    else:
        await message.answer_photo(photo=FSInputFile('image/menu.jpg', filename='кру'),
                            caption=f'Приветствую тебя в боте любви!\n'
                            f'Уже бежишь к своей половинке?',
                            reply_markup=keyboard_menu_true)
    print((int(decode_payload(message.text[7:])))!=message.from_user.id)
    if (message.text[7:])!="" and (int(decode_payload(message.text[7:])))!=message.from_user.id:
        zamena_para(int(decode_payload(message.text[7:])), message.from_user.id)
        await message.answer(f'Теперь ВЫ и {from_bd(1, int(decode_payload(message.text[7:])))} пара!')

@router.callback_query(F.data=="button_return")
async def start_cm(callback: CallbackQuery):
    if from_bd(4, callback.message.chat.id)==None:
        await callback.message.answer_photo(photo=FSInputFile('image/menu.jpg', filename='кру'),
                        caption=f'Приветствую тебя в боте любви!\n'
                        f'Для построения отношений выберите "Создать отношения"',
                        reply_markup=keyboard_menu
                        )
    else:
        await callback.message.answer_photo(photo=FSInputFile('image/menu.jpg', filename='кру'),
                            caption=f'Приветствую тебя в боте любви!\n'
                            f'Уже бежишь к своей половинке?',
                            reply_markup=keyboard_menu_true)



#кнопка соззать отношения
@router.callback_query(F.data=='button_new_otn')
async def mt_referal_menu (callback: CallbackQuery, state: FSMContext, bot: Bot):
    link = await create_start_link(bot,str(callback.from_user.id), encode=True)
    print("f")
    print(link)
    await callback.message.edit_caption(caption=f'Для того, что бы добавить пару\n'
                         f'Ваша половинка должна перейти по следующей ссылке:\n'
                         f'{link}',
                         media=FSInputFile('image/love.jpg'),
                         reply_markup=keyboard_menu_return
                        )
    await callback.answer()

#смена кнопки по проходу меню-отношения-----------------edit
@router.callback_query(F.data=='button_my_otn')
async def process_button_buy_press(callback: CallbackQuery):
    if callback.message.text != "Ваши отношения":
        if from_bd(4, callback.from_user.id):
            await callback.message.edit_caption(
                caption=f'Ваши отношения:\n'
                f'Ваша пара {from_bd(1, callback.from_user.id)}\n'
                f'Уровень отношений: {from_bd(6, callback.from_user.id)}\n'
                f'Прогресс: {from_bd(5, callback.from_user.id)}\n'
                f'Любовь творит чудеса!\n'
                f'Поцеловать свою половинку: /chmok',
                reply_markup=keyboard_menu_otn
        )
    await callback.answer()

@router.callback_query(F.data=="button_del_otn")
async def start_cm(callback: CallbackQuery):
    print(callback.from_user.id)
    del_otn(callback.from_user.id, from_bd(4, callback.from_user.id))
    await callback.answer(f'Отношения удалены💔')