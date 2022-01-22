import sys
from os.path import dirname, join, abspath
from telebot import types
from datetime import datetime

import EmojiAlphabet

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from SoftUbot import TIME as time
from SoftUbot.settings import conn, cursor


def homework_main():
    keyboard_student_hw = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Выбрать предмет \U000027A1', callback_data='choose_subject')

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

    keyboard_student_hw.add(key_1)
    keyboard_student_hw.add(key_back)

    msg = 'Хорошо, выберите, что вы хотите сделать?'

    return keyboard_student_hw, msg
