import sys
from os.path import dirname, join, abspath
from telebot import types
from datetime import datetime

import EmojiAlphabet

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from SoftUbot import TIME as time
from SoftUbot.settings import conn, cursor


def lk_teacher():

    keyboard_lk = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text= '\U0001F464 Мои данные' , callback_data='my_information')
    key_2 = types.InlineKeyboardButton(text= '\U0000260E Обратиться в поддержку' , callback_data='support')

    key_back = types.InlineKeyboardButton(text= EmojiAlphabet.back, callback_data='back_main_menu')

    keyboard_lk.add(key_1)
    keyboard_lk.add(key_2)
    keyboard_lk.add(key_back)

    msg = 'Вот Ваш личный кабинет:'

    return keyboard_lk, msg




def lk(info):
    msg = f"Моё ФИО - <b>{info['username']}</b>\n\nМой статус - <b>{info['status']}" \
          f"</b>\n\nМоя кафедра - <b>{info['department']}</b>"

    keyboard_lk_information_teacher = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='\U0000270D Редактировать данные', callback_data='change_account')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

    keyboard_lk_information_teacher.add(key_1)
    keyboard_lk_information_teacher.add(key_back)
    return  keyboard_lk_information_teacher, msg


def change_account(username):
    keyboard_change_profile = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='\U0000270D Изменить ФИО', callback_data='change_name')
    key_2 = types.InlineKeyboardButton(text='\U0000270D Изменить пароль', callback_data='change_password')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

    keyboard_change_profile.add(key_1, key_2)
    keyboard_change_profile.add(key_back)

    msg =  "Окей, <b>{}</b>! \nЧто Вы хотите поменять?".format(username)

    return keyboard_change_profile, msg







