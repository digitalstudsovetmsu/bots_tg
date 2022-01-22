import sys
from os.path import dirname, join, abspath
from telebot import types
from datetime import datetime
import math
import EmojiAlphabet

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from SoftUbot import TIME as time
from SoftUbot.settings import conn, cursor


def homework_main():
    keyboard_teacher_hw = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Создать\U0001F4DD', callback_data='create_hw')
    key_2 = types.InlineKeyboardButton(text='Изменить\U0001F527', callback_data='change_hw')
    key_3 = types.InlineKeyboardButton(text='Удалить\U0001F5D1', callback_data='delete_hw')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

    keyboard_teacher_hw.add(key_1)
    keyboard_teacher_hw.add(key_2, key_3)
    keyboard_teacher_hw.add(key_back)

    msg = 'Хорошо, выберите, что вы хотите сделать?'

    return keyboard_teacher_hw, msg


def department_subjects(department):
    cursor.execute("SELECT {} FROM table_info ".format(department))
    department = [item[0] for item in cursor.fetchall()]
    conn.commit()
    subjects = list(filter(None, department))

    keyboard = types.InlineKeyboardMarkup()
    n = len(subjects)

    if n % 2 == 0:
        while n > 0:
            key1 = types.InlineKeyboardButton(text=subjects[n - 1], callback_data=subjects[n - 1])
            key2 = types.InlineKeyboardButton(text=subjects[n - 2], callback_data=subjects[n - 2])
            keyboard.add(key1, key2)
            n -= 2

        key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')
        keyboard.add(key_back)
    else:
        while n > 1:
            key1 = types.InlineKeyboardButton(text=subjects[n - 1], callback_data=subjects[n - 1])
            key2 = types.InlineKeyboardButton(text=subjects[n - 2], callback_data=subjects[n - 2])
            keyboard.add(key1, key2)
            n -= 2

        key3 = types.InlineKeyboardButton(text=subjects[0], callback_data=subjects[0])
        key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')
        keyboard.add(key3)
        keyboard.add(key_back)

    msg = 'Выберите предмет:'

    return keyboard, msg


def change_homeworks(department):
    # вытаскивает все id-шники из таблицы с ДЗ по кафедре препода
    cursor.execute("SELECT id_hw FROM homework_all WHERE department = '{}' ORDER BY pub_date".format(department))
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

        data = 'prepod_change_{}'.format(id_hw[i - 1])
        key = types.InlineKeyboardButton(text=u"\U0001F4CD" + str(title),
                                         callback_data=data)
        keyboard.add(key)

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back,
                                          callback_data='back_hw_teacher')
    keyboard.add(key_back)

    msg = 'Выберите домашнее задание, которое нужно изменить:'

    return keyboard, msg


# print(change_homeworks('ЭММЭ'))

def delete_homeworks(department):
    # вытаскивает все id-шники из таблицы с ДЗ по кафедре препода
    cursor.execute("SELECT id_hw FROM homework_all WHERE department = '{}' ORDER BY pub_date".format(department))
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

        data = 'prepod_delete_{}'.format(id_hw[i - 1])
        key = types.InlineKeyboardButton(text=u"\U0001F4CD" + str(title),
                                         callback_data=data)
        keyboard.add(key)

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back,
                                          callback_data='back_hw_teacher')
    keyboard.add(key_back)

    msg = 'Выберите домашнее задание, которое нужно удалить:'

    return keyboard, msg


# --------------------------------------ДЛЯ СОЗДАНИЯ ДЗ ---------------------

def homework_groupe(page, group_list):
    length = len(group_list)  # длина списка всех групп

    max_page = math.ceil(length / 4)  # считаем сколько будет страниц для списка

    keyboard = types.InlineKeyboardMarkup()  # создаём клавиатуру

    if page == 1:  # передали 1-ю страницу

        # случай когда передано до 4-х групп
        if length <= 4:

            n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

            if n == 0:  # делиться с нулевым остатком только число 4, значит 4 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'hw_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'hw_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'hw_{group_list[page * 4 - 2]}')
                key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                                  callback_data=f'hw_{group_list[page * 4 - 1]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

                keyboard.add(key1, key2)
                keyboard.add(key3, key4)
                keyboard.add(key_menu)

            if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'hw_{group_list[page * 4 - 4]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

                keyboard.add(key1)
                keyboard.add(key_menu)

            if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'hw_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'hw_{group_list[page * 4 - 3]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

                keyboard.add(key1, key2)
                keyboard.add(key_menu)

            if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'hw_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'hw_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'hw_{group_list[page * 4 - 2]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

                keyboard.add(key1, key2)
                keyboard.add(key3)
                keyboard.add(key_menu)

        else:

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'hw_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'hw_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'hw_{group_list[page * 4 - 1]}')

            key_next = types.InlineKeyboardButton(text='\U000025B6',
                                                  callback_data='next_page_groupe_{}_hw'.format(page))

            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_next)
            keyboard.add(key_menu)


    elif max_page > page > 1:

        key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                          callback_data=f'hw_{group_list[page * 4 - 4]}')
        key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                          callback_data=f'hw_{group_list[page * 4 - 3]}')
        key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                          callback_data=f'hw_{group_list[page * 4 - 2]}')
        key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                          callback_data=f'hw_{group_list[page * 4 - 1]}')

        key_next = types.InlineKeyboardButton(text='\U000025B6', callback_data='next_page_groupe_{}_hw'.format(page))
        key_back = types.InlineKeyboardButton(text='\U000025C0', callback_data='back_page_groupe_{}_hw'.format(page))
        key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

        keyboard.add(key1, key2)
        keyboard.add(key3, key4)

        keyboard.add(key_back, key_next)
        keyboard.add(key_menu)

    else:

        n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

        if n == 0:  # делиться с нулевым остатком только числа кратные 4-м

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'hw_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'hw_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'hw_{group_list[page * 4 - 1]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_hw'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_{group_list[page * 4 - 4]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_hw'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

            keyboard.add(key1)
            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'hw_{group_list[page * 4 - 3]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_hw'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

            keyboard.add(key1, key2)
            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'hw_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'hw_{group_list[page * 4 - 2]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_hw'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

            keyboard.add(key1, key2)
            keyboard.add(key3)
            keyboard.add(key_back)
            keyboard.add(key_menu)

    msg = 'Выберите группу, для которой предназначено домашнее задание:'

    return keyboard, msg


def create_title(title):  # после ввода заголовка
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='\U0000270F Текст для ДЗ', callback_data='create_text_hw')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

    keyboard.add(key_1)
    keyboard.add(key_back)

    msg = '\U0001F4DA<code>Домашнее задание:</code>\n\n\U0001F4CD<b>Заголовок:</b> "{}"\n\n\U0000270F<b>Текст домашнего задания:</b>\n<i>Не заполнен</i>'.format(
        title)
    return keyboard, msg


def homework_content(teacher, groupe, department, title, text, deadline_d, deadline_t, file):  # после ввода текста
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
    key_1 = types.InlineKeyboardButton(text='Дедлайн ДАТА \U0001F4C5', callback_data='deadline_d')
    key_2 = types.InlineKeyboardButton(text='Дедлайн ВРЕМЯ \U000023F0', callback_data='deadline_t')
    key_3 = types.InlineKeyboardButton(text='Файл' + u"\U0001F4C4", callback_data='plus_file')
    key_4 = types.InlineKeyboardButton(text='Подтвердить \U00002705', callback_data='confirm')

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

    keyboard.add(key_1, key_2)
    keyboard.add(key_3)
    keyboard.add(key_4)
    keyboard.add(key_back)

    return keyboard, msg, file


def back_to_hw_content():
    keyboard = types.InlineKeyboardMarkup()
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_content')
    keyboard.add(key_back)

    return keyboard


# ------------------------------- ДЛЯ ИЗМЕНЕНИЯ ДЗ --------------------------------------
def homework_change_content(id_hw, teacher, groupe, department, title, text, deadline_d, deadline_t,
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
    key_1 = types.InlineKeyboardButton(text='Заголовок \U0001F4CD', callback_data='title_change'.format(id_hw))
    key_2 = types.InlineKeyboardButton(text='Текст \U0000270F', callback_data='text_change'.format(id_hw))
    key_3 = types.InlineKeyboardButton(text='Дедлайн ДАТА \U0001F4C5', callback_data='deadline_d_change'.format(id_hw))
    key_4 = types.InlineKeyboardButton(text='Дедлайн ВРЕМЯ \U000023F0', callback_data='deadline_t_change'.format(id_hw))
    key_5 = types.InlineKeyboardButton(text='Файл' + u"\U0001F4C4", callback_data='file_change'.format(id_hw))
    key_6 = types.InlineKeyboardButton(text='Группа \U0001F465', callback_data='groupe_change'.format(id_hw))

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

    keyboard.add(key_1, key_2)
    keyboard.add(key_6)
    keyboard.add(key_3, key_4)
    keyboard.add(key_5)
    keyboard.add(key_back)

    return keyboard, msg, file


def back_to_change_hw_content(id_hw):
    keyboard = types.InlineKeyboardMarkup()
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_content{}'.format(id_hw))
    keyboard.add(key_back)

    return keyboard


def homework_groupe_change(page, group_list):
    length = len(group_list)  # длина списка всех групп

    max_page = math.ceil(length / 4)  # считаем сколько будет страниц для списка

    keyboard = types.InlineKeyboardMarkup()  # создаём клавиатуру

    if page == 1:  # передали 1-ю страницу

        # случай когда передано до 4-х групп
        if length <= 4:

            n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

            if n == 0:  # делиться с нулевым остатком только число 4, значит 4 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 2]}')
                key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 1]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

                keyboard.add(key1, key2)
                keyboard.add(key3, key4)
                keyboard.add(key_menu)

            if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 4]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

                keyboard.add(key1)
                keyboard.add(key_menu)

            if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 3]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

                keyboard.add(key1, key2)
                keyboard.add(key_menu)

            if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'hw_change_{group_list[page * 4 - 2]}')
                key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

                keyboard.add(key1, key2)
                keyboard.add(key3)
                keyboard.add(key_menu)

        else:

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_change_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'hw_change_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'hw_change_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'hw_change_{group_list[page * 4 - 1]}')

            key_next = types.InlineKeyboardButton(text='\U000025B6',
                                                  callback_data='next_page_groupe_{}_hw_change_'.format(page))

            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_next)
            keyboard.add(key_menu)


    elif max_page > page > 1:

        key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                          callback_data=f'hw_change_{group_list[page * 4 - 4]}')
        key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                          callback_data=f'hw_change_{group_list[page * 4 - 3]}')
        key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                          callback_data=f'hw_change_{group_list[page * 4 - 2]}')
        key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                          callback_data=f'hw_change_{group_list[page * 4 - 1]}')

        key_next = types.InlineKeyboardButton(text='\U000025B6',
                                              callback_data='next_page_groupe_{}_hw_change_'.format(page))
        key_back = types.InlineKeyboardButton(text='\U000025C0',
                                              callback_data='back_page_groupe_{}_hw_change_'.format(page))
        key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

        keyboard.add(key1, key2)
        keyboard.add(key3, key4)

        keyboard.add(key_back, key_next)
        keyboard.add(key_menu)

    else:

        n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

        if n == 0:  # делиться с нулевым остатком только числа кратные 4-м

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_change_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'hw_change_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'hw_change_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'hw_change_{group_list[page * 4 - 1]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_hw_change_'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_change_{group_list[page * 4 - 4]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_hw_change_'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

            keyboard.add(key1)
            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_change_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'hw_change_{group_list[page * 4 - 3]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_hw_change_'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

            keyboard.add(key1, key2)
            keyboard.add(key_back)
            keyboard.add(key_menu)

        if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'hw_change_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'hw_change_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'hw_change_{group_list[page * 4 - 2]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0',
                                                  callback_data='back_page_groupe_{}_hw_change_'.format(page))
            key_menu = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_change_teacher')

            keyboard.add(key1, key2)
            keyboard.add(key3)
            keyboard.add(key_back)
            keyboard.add(key_menu)

    msg = 'Выберите группу, для которой предназначено домашнее задание:'

    return keyboard, msg

# ---------------------------- ДЛЯ УДАЛЕНИЯ ДЗ -------------------------

def homework_delete_content(id_hw, teacher, groupe, department, title, text, deadline_d, deadline_t,
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
    key_1 = types.InlineKeyboardButton(text='Удалить', callback_data='delete_hw_to_hw_id'.format(id_hw))

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_hw_teacher')

    keyboard.add(key_1)
    keyboard.add(key_back)

    return keyboard, msg, file

