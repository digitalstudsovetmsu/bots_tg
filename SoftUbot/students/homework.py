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


def groupe_subjects(groupe):
    course = str(groupe)[0]

    cursor.execute("SELECT course_{} FROM table_info ".format(course))
    choose_subject = [item[0] for item in cursor.fetchall()]
    conn.commit()
    subjects = list(filter(None, choose_subject))

    keyboard = types.InlineKeyboardMarkup()
    n = len(subjects)

    if n % 2 == 0:
        while n > 0:
            key1 = types.InlineKeyboardButton(text=subjects[n - 1], callback_data=subjects[n - 1])
            key2 = types.InlineKeyboardButton(text=subjects[n - 2], callback_data=subjects[n - 2])
            keyboard.add(key1, key2)
            n -= 2

        key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_student')
        keyboard.add(key_back)
    else:
        while n > 1:
            key1 = types.InlineKeyboardButton(text=subjects[n - 1], callback_data=subjects[n - 1])
            key2 = types.InlineKeyboardButton(text=subjects[n - 2], callback_data=subjects[n - 2])
            keyboard.add(key1, key2)
            n -= 2

        key3 = types.InlineKeyboardButton(text=subjects[0], callback_data=subjects[0])
        key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_student')
        keyboard.add(key3)
        keyboard.add(key_back)

    msg = 'Выберай предмет:'

    return keyboard, msg


def view_homework(subject):
    cursor.execute("SELECT id_hw FROM homework_all WHERE subject = '{}' ORDER BY pub_date".format(subject))
    id_hw = [item[0] for item in cursor.fetchall()]
    conn.commit()
    # считаает их кол-во
    n = len(id_hw)

    # создаёт клаву
    keyboard = types.InlineKeyboardMarkup()

    # создаёт кнопки по chatid + номер, текстом для кнопки служит Заголовок
    for i in list(range(n)):
        cursor.execute("SELECT title FROM homework_all WHERE id_hw = {}".format(id_hw[i - 1]))
        title = [item[0] for item in cursor.fetchall()][0]
        conn.commit()

        data = 'student_view_{}'.format(id_hw[i - 1])
        key = types.InlineKeyboardButton(text=u"\U0001F4CD" + str(title),
                                         callback_data=data)
        keyboard.add(key)

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back,
                                          callback_data='back_hw_student')
    keyboard.add(key_back)

    msg = 'Какое ДЗ ты хочешь посмотреть?'

    return keyboard, msg


def homework_view_content(teacher, groupe, department, title, text, deadline_d, deadline_t,
                          file):  # после ввода текста
    msg = '\U0001F4DA<b>Домашнее задание:</b>\n\n' \
          '\U0001F468\U0000200D\U0001F3EB <code>Преподаватель:</code> {} (кафедра: {})\n\n' \
          '\U0001F465  <code>Группа:</code> {}\n\n' \
          '\U0001F4CD <code>Заголовок:</code> "{}"\n\n' \
          '\U0000270F <code>Текст домашнего задания:</code>\n\n' \
          '    {}\n\n' \
          '\U000023F0 <code>Дедлайн:</code>\n' \
          '       - Дата: <i>{}</i>\n' \
          '       - Время: <i>{}</i>\n\n' \
          '\U0001F4CE <code>Файл</code> - <i>{}</i>' \
        .format(teacher, department, groupe, title, text, deadline_d, deadline_t, file)

    keyboard = types.InlineKeyboardMarkup()
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_student')

    keyboard.add(key_back)

    return keyboard, msg, file
