import sys
from os.path import dirname, join, abspath
from telebot import types
from datetime import datetime

import EmojiAlphabet

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from SoftUbot import TIME as time
from SoftUbot.settings import conn, cursor


def check_me(groupe):
    seychas = time.schedule_now(datetime.now(), groupe)

    if not seychas[1]:
        msg = 'Я не могу тебя отметить, так как сейчас нет пары! Когда у тебя начнётся пара, ты сможешь отметиться!'
        keyboard_menu_back = types.InlineKeyboardMarkup()

        key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

        keyboard_menu_back.add(key_back)

        return keyboard_menu_back, msg
    else:
        msg = 'Сейчас у тебя - <b> {}! </b> \n\nВедёт пару -  <b>{}.</b> \n\n А проходит это в<b> {} </b>кабинете'.format(
            seychas[0]['name'], seychas[0]['teacher'], seychas[0]['cab'])

        keyboard_check_me = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Отметиться', callback_data='check_para')
        key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

        keyboard_check_me.add(key_1)
        keyboard_check_me.add(key_back)

        return keyboard_check_me, msg


def send_geo():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_location = types.KeyboardButton(text="Отправить геопозицию", request_location=True)
    keyboard.add(button_location)

    msg = 'Хорошо, чтобы отметиться, нужно подтвертить своё местоположение! Отправь мне свою геопозицию!'

    return keyboard, msg


def for_location(chat_id):
    keyboard = types.ReplyKeyboardRemove()
    para = time.number_para(datetime.now())

    cursor.execute("SELECT groupe FROM all_in_one WHERE id_telegram = {}".format(chat_id))
    groupe = int(([item[0] for item in cursor.fetchall()][0]))
    conn.commit()

    course = int(str(groupe)[0])

    if not para == 0:

        if para == 1:
            cursor.execute("UPDATE otmetka{} SET firstP = TRUE where chatid = {}".format(course, chat_id))
            conn.commit()
        if para == 2:
            cursor.execute("UPDATE otmetka{} SET secondP = TRUE where chatid = {}".format(course, chat_id))
            conn.commit()
        if para == 3:
            cursor.execute("UPDATE otmetka{} SET thirdP = TRUE where chatid = {}".format(course, chat_id))
            conn.commit()
        if para == 4:
            cursor.execute("UPDATE otmetka{} SET fourP = TRUE where chatid = {}".format(course, chat_id))
            conn.commit()
        if para == 5:
            cursor.execute("UPDATE otmetka{} SET FiveP = TRUE where chatid = {}".format(course, chat_id))
            conn.commit()

            msg = "Я тебя отметил на {} паре!".format(para)

            return keyboard, msg

    else:
        msg = 'Я тебя не могу отметить! Видимо, пара уже закончилась)))'

        keyboard_menu_back = types.InlineKeyboardMarkup()

        key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

        keyboard_menu_back.add(key_back)

        return keyboard_menu_back, msg


# for_location(323739054)
