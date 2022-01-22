import sys
import math
from os.path import dirname, join, abspath
from telebot import types
from datetime import datetime

import EmojiAlphabet

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from SoftUbot import TIME as time
from SoftUbot.settings import conn, cursor


def lk_student():
    keyboard_lk = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text='\U0001F464 Мои данные', callback_data='my_information')
    key_2 = types.InlineKeyboardButton(text='\U0000260E Обратиться в поддержку', callback_data='support')

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

    keyboard_lk.add(key_1)
    keyboard_lk.add(key_2)
    keyboard_lk.add(key_back)

    msg = 'Вот твой личный кабинет:'

    return keyboard_lk, msg


def lk(info):

    msg = f"Моё ФИО - <b>{info['username']}</b>\n\nМой статус - <b>{info['status']}</b>\n\nМоя группа - <b>{info['groupe']}</b>, \n\n <b>Я староста!</b>"

    keyboard_lk_information_student = types.InlineKeyboardMarkup()
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

    keyboard_lk_information_student.add(key_back)

    return keyboard_lk_information_student, msg


def lk_no_leader(info):
    msg = f"Моё ФИО - <b>{info['username']}</b>\n\nМой статус - <b>{info['status']}" \
          f"</b>\n\nМоя группа - <b>{info['groupe']}</b>"

    keyboard_lk_information_student = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text='\U0000270D Редактировать данные', callback_data='change_account')
    key_2 = types.InlineKeyboardButton(text='\U0001F57A Стать старостой \U0001F483', callback_data='change_leader')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

    keyboard_lk_information_student.add(key_1, key_2)
    keyboard_lk_information_student.add(key_back)

    return keyboard_lk_information_student, msg

def change_account(username):
    keyboard_change_profile = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='\U0000270D Изменить ФИО', callback_data='change_name')
    key_2 = types.InlineKeyboardButton(text='\U0000270D Изменить пароль', callback_data='change_password')
    key_3 = types.InlineKeyboardButton(text='\U0000270D Изменить группу', callback_data='change_groupe')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

    keyboard_change_profile.add(key_1, key_2, key_3)
    keyboard_change_profile.add(key_back)

    msg = "Окей, <b>{}</b>! \nЧто ты хочешь поменять?".format(username)

    return keyboard_change_profile, msg


def change_groupe(page, group_list):
    length = len(group_list)  # длина списка всех групп

    max_page = math.ceil(length / 4)  # считаем сколько будет страниц для списка

    keyboard = types.InlineKeyboardMarkup()  # создаём клавиатуру

    if page == 1:  # передали 1-ю страницу

        # случай когда передано до 4-х групп
        if length <= 4:

            n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

            if n == 0:  # делиться с нулевым остатком только число 4, значит 4 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'change_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'change_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'change_{group_list[page * 4 - 2]}')
                key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                                  callback_data=f'change_{group_list[page * 4 - 1]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

                keyboard.add(key1, key2)
                keyboard.add(key3, key4)
                keyboard.add(key_menu)

            if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'change_{group_list[page * 4 - 4]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

                keyboard.add(key1)
                keyboard.add(key_menu)


            if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'change_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'change_{group_list[page * 4 - 3]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

                keyboard.add(key1, key2)
                keyboard.add(key_menu)

            if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'change_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'change_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'change_{group_list[page * 4 - 2]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

                keyboard.add(key1, key2)
                keyboard.add(key3)
                keyboard.add(key_menu)

        else:

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'change_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'change_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'change_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'change_{group_list[page * 4 - 1]}')

            key_next = types.InlineKeyboardButton(text='\U000025B6',
                                                  callback_data='next_page_groupe_{}_change'.format(page))

            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_next)
            keyboard.add(key_menu)


    elif max_page > page > 1:

        key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                          callback_data=f'change_{group_list[page * 4 - 4]}')
        key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                          callback_data=f'change_{group_list[page * 4 - 3]}')
        key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                          callback_data=f'change_{group_list[page * 4 - 2]}')
        key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                          callback_data=f'change_{group_list[page * 4 - 1]}')

        key_next = types.InlineKeyboardButton(text='\U000025B6', callback_data='next_page_groupe_{}_change'.format(page))
        key_back = types.InlineKeyboardButton(text='\U000025C0', callback_data='back_page_groupe_{}_change'.format(page))
        key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

        keyboard.add(key1, key2)
        keyboard.add(key3, key4)

        keyboard.add(key_back, key_next)
        keyboard.add(key_menu)

    else:

        n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

        if n == 0:  # делиться с нулевым остатком только числа кратные 4-м

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'change_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'change_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'change_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'change_{group_list[page * 4 - 1]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_change'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'change_{group_list[page * 4 - 4]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_change'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')


            keyboard.add(key1)
            keyboard.add(key_back)
            keyboard.add(key_menu)


        if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'change_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'change_{group_list[page * 4 - 3]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_change'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

            keyboard.add(key1, key2)
            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'change_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'change_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'change_{group_list[page * 4 - 2]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_change'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

            keyboard.add(key1, key2)
            keyboard.add(key3)
            keyboard.add(key_back)
            keyboard.add(key_menu)

    msg = 'Выберите группу, которая Вам интересена:'

    return keyboard, msg



