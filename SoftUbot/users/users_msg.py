#
#
# в этом файле храняться все сообщения от бота и все клавиатуры
import math
from telebot import types
import EmojiAlphabet


# ------------------------------------------------
def home():  # первое сообщение при отсутсвии регистрации
    keyboard_register = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text='\U0001F6AA Войти', callback_data='go_login')
    key_2 = types.InlineKeyboardButton(text='\U0000260E Контакты', callback_data='contacts')
    key_3 = types.InlineKeyboardButton(text='\U00002139 О нас', callback_data='info_no_reg')

    keyboard_register.add(key_1)
    keyboard_register.add(key_2, key_3)

    msg = 'Вы пока не зарегистрированы, пройдите регистрацию:'

    return keyboard_register, msg


# ------------------------------------------------
def teacher_or_student():  # выбор учитель или ученик при регистрации
    keyboard_teacher_student = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text='\U0001F468\U0000200D\U0001F393 Студент', callback_data='student')
    key_2 = types.InlineKeyboardButton(text='\U0001F468\U0000200D\U0001F3EB Преподаватель', callback_data='teacher')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_home')

    keyboard_teacher_student.add(key_1, key_2)
    keyboard_teacher_student.add(key_back)

    msg = 'Для начала укажите, кем вы являетесь?'

    return keyboard_teacher_student, msg


# ------------------------------------------------
def home_back():  # клавиатура "назад"
    keyboard_reg_back = types.InlineKeyboardMarkup()

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_home')

    keyboard_reg_back.add(key_back)

    return keyboard_reg_back


# ------------------------------------ Когда выбрали СТУДЕНТА ----------------------
def student():
    keyboard = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text='\U0001F513 Авторизация ', callback_data='auth_student')
    key_2 = types.InlineKeyboardButton(text='\U0001F510 Регистрация', callback_data='reg_student')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='go_login')

    keyboard.add(key_1, key_2)
    keyboard.add(key_back)

    msg = 'У тебя уже есть аккаунт в нашем приложении?'

    return keyboard, msg


# -----------------------------------
def student_back():  # клавиатура "назад"
    keyboard_back = types.InlineKeyboardMarkup()

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_student')

    keyboard_back.add(key_back)

    return keyboard_back


# ------------------------------------ Когда выбрали РЕГИТСРАЦИЮ    СТУДЕНТА ----------------------

# -------------------------------------------------------
#
#
# Для username отдельная функция не используется
#
#
# -------------------------------------------------------


# ------------------------------------------------ клава и сообщение после выбора username ------
def reg_student_after_username(username):
    keyboard_student = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text='Установить пароль', callback_data='reg_password')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_student')

    keyboard_student.add(key_1)
    keyboard_student.add(key_back)

    msg = 'Рад познакомиться, <b>{}</b> !'.format(username)

    return keyboard_student, msg


# -------------------------------------------------------
#
#
# Для password отдельная функция не используется
#
#
# -------------------------------------------------------

def reg_student_after_password():
    keyboard_student = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text='Выбрать группу', callback_data='reg_groupe')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_student')

    keyboard_student.add(key_1)
    keyboard_student.add(key_back)

    msg = 'Твой пароль успешно сохранён!'

    return keyboard_student, msg


# ------------------------------------------------------- клава с выбором группы -------------

def reg_group(page, group_list):
    length = len(group_list)  # длина списка всех групп

    max_page = math.ceil(length / 4)  # считаем сколько будет страниц для списка

    keyboard = types.InlineKeyboardMarkup()  # создаём клавиатуру

    if page == 1:  # передали 1-ю страницу

        # случай когда передано до 4-х групп
        if length <= 4:

            n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

            if n == 0:  # делиться с нулевым остатком только число 4, значит 4 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'reg_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'reg_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'reg_{group_list[page * 4 - 2]}')
                key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                                  callback_data=f'reg_{group_list[page * 4 - 1]}')

                keyboard.add(key1, key2)
                keyboard.add(key3, key4)

            if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'reg_{group_list[page * 4 - 4]}')

                keyboard.add(key1)

            if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'reg_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'reg_{group_list[page * 4 - 3]}')

                keyboard.add(key1, key2)

            if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

                key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                                  callback_data=f'reg_{group_list[page * 4 - 4]}')
                key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                                  callback_data=f'reg_{group_list[page * 4 - 3]}')
                key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                                  callback_data=f'reg_{group_list[page * 4 - 2]}')

                keyboard.add(key1, key2)
                keyboard.add(key3)

        else:

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'reg_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'reg_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'reg_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'reg_{group_list[page * 4 - 1]}')

            key_next = types.InlineKeyboardButton(text='\U000025B6', callback_data='next_page_groupe_{}'.format(page))

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_next)


    elif max_page > page > 1:

        key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                          callback_data=f'reg_{group_list[page * 4 - 4]}')
        key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                          callback_data=f'reg_{group_list[page * 4 - 3]}')
        key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                          callback_data=f'reg_{group_list[page * 4 - 2]}')
        key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                          callback_data=f'reg_{group_list[page * 4 - 1]}')

        key_next = types.InlineKeyboardButton(text='\U000025B6', callback_data='next_page_groupe_{}'.format(page))
        key_back = types.InlineKeyboardButton(text='\U000025C0', callback_data='back_page_groupe_{}'.format(page))

        keyboard.add(key1, key2)
        keyboard.add(key3, key4)

        keyboard.add(key_back, key_next)


    else:

        n = length % 4  # делим с остатком, этот остаток и будет нужное нам число кнопок

        if n == 0:  # делиться с нулевым остатком только числа кратные 4-м

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'reg_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'reg_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'reg_{group_list[page * 4 - 2]}')
            key4 = types.InlineKeyboardButton(text=group_list[page * 4 - 1],
                                              callback_data=f'reg_{group_list[page * 4 - 1]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0', callback_data='back_page_groupe_{}'.format(page))

            keyboard.add(key1, key2)
            keyboard.add(key3, key4)

            keyboard.add(key_back)

        if n == 1:  # делиться с нулевым остатком только число 1, значит 1 кнопка

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'reg_{group_list[page * 4 - 4]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0', callback_data='back_page_groupe_{}'.format(page))

            keyboard.add(key1)
            keyboard.add(key_back)

        if n == 2:  # делиться с нулевым остатком только число 2, значит 2 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'reg_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'reg_{group_list[page * 4 - 3]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0', callback_data='back_page_groupe_{}'.format(page))

            keyboard.add(key1, key2)
            keyboard.add(key_back)

        if n == 3:  # делиться с нулевым остатком только число 3, значит 3 кнопки

            key1 = types.InlineKeyboardButton(text=group_list[page * 4 - 4],
                                              callback_data=f'reg_{group_list[page * 4 - 4]}')
            key2 = types.InlineKeyboardButton(text=group_list[page * 4 - 3],
                                              callback_data=f'reg_{group_list[page * 4 - 3]}')
            key3 = types.InlineKeyboardButton(text=group_list[page * 4 - 2],
                                              callback_data=f'reg_{group_list[page * 4 - 2]}')

            key_back = types.InlineKeyboardButton(text='\U000025C0', callback_data='back_page_groupe_{}'.format(page))

            keyboard.add(key1, key2)
            keyboard.add(key3)
            keyboard.add(key_back)

    msg = 'Выбирай свою группу:'

    return keyboard, msg


def end_reg(course, groupe):  # завершение регистрации
    msg_1 = f'Отлично, вы выбрали {course}0{groupe} группу.'
    msg_2 = 'Спасибо за прохождение регистрации. Теперь ты можешь пользоваться всем функционалом SoftU'
    msg_3 = 'Вот моё главное меню:'

    keyboard_menu_student = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text=EmojiAlphabet.information + ' О нас ' + EmojiAlphabet.information,
                                       callback_data='info')
    key_2 = types.InlineKeyboardButton(text=EmojiAlphabet.profile + ' Личный кабинет ' + EmojiAlphabet.profile,
                                       callback_data='kabinet')
    key_3 = types.InlineKeyboardButton(text=EmojiAlphabet.bets + ' Расписание' + EmojiAlphabet.bets,
                                       callback_data='schedule')
    key_4 = types.InlineKeyboardButton(text=u"\U00002705" + ' Отметиться ' + u"\U00002705", callback_data='checked_me')
    key_5 = types.InlineKeyboardButton(text=u"\U0001F4D5" + ' Домашнее задание ' + u"\U0001F4D7",
                                       callback_data='home_work')

    keyboard_menu_student.add(key_3, key_4)
    keyboard_menu_student.add(key_5)
    keyboard_menu_student.add(key_2)
    keyboard_menu_student.add(key_1)

    return keyboard_menu_student, msg_1, msg_2, msg_3


# ------------------------------------ ПРЕПОДАВАТЕЛЬ----------------------

def teacher():
    keyboard = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text='\U0001F513 Авторизация ', callback_data='auth_teacher')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='go_login')

    keyboard.add(key_1)
    keyboard.add(key_back)

    msg = 'У Вас уже должен быть аккаунт в нашем приложении.'

    return keyboard, msg


# -----------------------------------


# ------------------------------------ Личный кабинет----------------------

def back_to_lk():  # клавиатура "назад"

    keyboard_back = types.InlineKeyboardMarkup()

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_lk')

    keyboard_back.add(key_back)

    return keyboard_back
