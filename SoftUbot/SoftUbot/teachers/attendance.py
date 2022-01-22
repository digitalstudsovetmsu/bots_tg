import math
from telebot import types
import sys
from os.path import dirname, join, abspath
from datetime import datetime



sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from SoftUbot import TIME as time
from SoftUbot.settings import conn, cursor

import EmojiAlphabet


def check_groupe(page, group_list):
    length = len(group_list)  # длина списка всех групп

    max_page = math.ceil(length / 4)  # считаем сколько будет страниц для списка

    keyboard = types.InlineKeyboardMarkup()  # создаём клавиатуру

    if page == 1:  # передали 1-ю страницу

        # случай когда передано до 4-х групп
        if length <= 4:

            n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

            if n == 0:  # делиться с нулевым остатком только число 4, значит 4 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'check_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'check_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'check_{group_list[page * 4 - 2]}')
                key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                                  callback_data=f'check_{group_list[page * 4 - 1]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

                keyboard.add(key1, key2)
                keyboard.add(key3, key4)
                keyboard.add(key_menu)

            if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'check_{group_list[page * 4 - 4]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

                keyboard.add(key1)
                keyboard.add(key_menu)


            if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'check_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'check_{group_list[page * 4 - 3]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

                keyboard.add(key1, key2)
                keyboard.add(key_menu)

            if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'check_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'check_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'check_{group_list[page * 4 - 2]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

                keyboard.add(key1, key2)
                keyboard.add(key3)
                keyboard.add(key_menu)

        else:

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'check_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'check_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'check_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'check_{group_list[page * 4 - 1]}')

            key_next = types.InlineKeyboardButton(text='\U000025B6',
                                                  callback_data='next_page_groupe_{}_check'.format(page))

            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_next)
            keyboard.add(key_menu)


    elif max_page > page > 1:

        key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                          callback_data=f'check_{group_list[page * 4 - 4]}')
        key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                          callback_data=f'check_{group_list[page * 4 - 3]}')
        key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                          callback_data=f'check_{group_list[page * 4 - 2]}')
        key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                          callback_data=f'check_{group_list[page * 4 - 1]}')

        key_next = types.InlineKeyboardButton(text='\U000025B6', callback_data='next_page_groupe_{}_check'.format(page))
        key_back = types.InlineKeyboardButton(text='\U000025C0', callback_data='back_page_groupe_{}_check'.format(page))
        key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

        keyboard.add(key1, key2)
        keyboard.add(key3, key4)

        keyboard.add(key_back, key_next)
        keyboard.add(key_menu)

    else:

        n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

        if n == 0:  # делиться с нулевым остатком только числа кратные 4-м

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'check_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'check_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'check_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'check_{group_list[page * 4 - 1]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_check'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'check_{group_list[page * 4 - 4]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_check'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')


            keyboard.add(key1)
            keyboard.add(key_back)
            keyboard.add(key_menu)


        if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'check_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'check_{group_list[page * 4 - 3]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_check'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

            keyboard.add(key1, key2)
            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'check_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'check_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'check_{group_list[page * 4 - 2]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_check'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

            keyboard.add(key1, key2)
            keyboard.add(key3)
            keyboard.add(key_back)
            keyboard.add(key_menu)

    msg = 'Выберите группу, которая Вам интересена:'

    return keyboard, msg

def table_otmetka(group):
    # вытаскивает нынешнюю дату (число, месяц, час, минуты)
    date = datetime.now().strftime("%d.%m (%H %M)")

    # вытаскивает курс из группы
    course = int(str(group)[0])

    # если группа ровна целому числу, то вытаскивает весь курс
    if group == 100 or group == 200 or group == 300 or group == 400:

        cursor.execute(
            "SELECT 'ФИО','Первая пара','Вторая пара','Третья пара','Четвёртая пара','Пятая пара' "
            "UNION SELECT FIO,FirstP,SecondP,ThirdP,FourP,FiveP FROM otmetka{} "
            " INTO OUTFILE 'data_all{}.xls'".format(course, date))
        conn.commit()

        src = '/var/lib/mysql/SoftWare/data_all{}.xls'.format(date)
        doc = open(src, 'rb')

    # вытаскивает только отдельную группу
    else:

        cursor.execute("COPY (SELECT FIO,FirstP,SecondP,ThirdP,FourP,FiveP FROM otmetka{} WHERE gruppa = {} ) TO '/etc/postgresql/aaa.csv'".format(course, group))
        conn.commit()

        # src = '/etc/postgresql/aaa.csv'
        # doc = open(src, 'rb')

    return doc

# print(table_otmetka(203))