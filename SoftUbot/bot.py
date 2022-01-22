import telebot
# from telebot import types
# import TIME as time
#
# from datetime import datetime

import settings
# from settings import conn, cursor
import validation

from users import func_main
from users.models import User, RegistrationForm, LogInForm, Account
from teachers.models import Homework, ChangeHomework, DeleteHomowork
from users import users_msg

from students import students_msg
from students import check
from students import schedule as student_schedule
from students import homework as student_hw
from students import lk as student_lk
from students.models import StudentHomeworkView

from teachers import teachers_msg
from teachers import attendance
# from SoftUbot.teachers import schedule as teacher_schedule
from teachers import homework as teacher_hw
from teachers import lk as teacher_lk

bot = telebot.TeleBot(settings.BotToken)  # бот API


@bot.message_handler(commands=['start'])
def starter(message):
    chat_id = message.chat.id
    print(chat_id)

    if not func_main.new_session(chat_id):  # эта функция проверяет есть ли этотт chatid в бд

        bot.send_message(chat_id, settings.text_starter, parse_mode='html')
        bot.send_message(chat_id, users_msg.home()[1],
                         reply_markup=users_msg.home()[0])

    else:
        if not func_main.check_all_attr(chat_id):
            bot.send_message(chat_id, settings.text_starter, parse_mode='html')
            bot.send_message(chat_id, users_msg.home()[1],
                             reply_markup=users_msg.home()[0])
        else:
            try:
                user = User(chat_id)

                if user.is_teacher():

                    bot.send_message(message.chat.id, teachers_msg.main_menu(user.username())[1], parse_mode='html',
                                     reply_markup=teachers_msg.main_menu(user.username())[0])

                else:

                    bot.send_message(message.chat.id, students_msg.main_menu(user.username())[1], parse_mode='html',
                                     reply_markup=students_msg.main_menu(user.username())[0])

            except:
                print('Пользователь не найден')


# -------------------------------------- РЕГИСТРАЦИЯ --------------------------------------------------
def ask_username(message):  # устанавливает username
    username = message.text

    val = validation.validFIO(username)  # проверка валидационная
    if val == 'Всё отлично!':
        reg = RegistrationForm(int(message.chat.id))
        reg.update_username(username)

        msg = users_msg.reg_student_after_username(username)

        bot.send_message(message.chat.id, msg[1], parse_mode='html', reply_markup=msg[0])

    else:  # если не прошла валидацию, то ещё раз можно ввести
        msg = val
        msg2 = bot.send_message(message.chat.id, msg, parse_mode='html')
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg2, ask_username)


def ask_password(message):  # устанавливет password
    password = message.text

    val = validation.validPassword(password)  # проверка валидационная
    if val == 'Всё отлично!':
        reg = RegistrationForm(int(message.chat.id))
        reg.update_password(password)

        msg = users_msg.reg_student_after_password()

        bot.send_message(message.chat.id, msg[1], parse_mode='html', reply_markup=msg[0])

    else:  # если не прошла валидацию, то ещё раз можно ввести
        msg = val
        msg2 = bot.send_message(message.chat.id, msg, parse_mode='html')
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg2, ask_password)


def check_username(message):
    username = message.text
    check = func_main.check_username(username)
    if check == 'Всё отлично!':
        auth = LogInForm(int(message.chat.id))
        auth.update_username(username)

        msg = bot.send_message(message.chat.id, 'Введи свой пароль:', parse_mode='html')
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg, check_password)

    else:
        msg2 = bot.send_message(message.chat.id, check, parse_mode='html', reply_markup=users_msg.student_back())
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg2, check_username)


def check_password(message):
    password = message.text
    check = func_main.check_password(message.chat.id, password)
    if check == 'Всё отлично!':
        auth = LogInForm(int(message.chat.id))
        auth.update_password(password)
        auth.move_to_all_in_one()

        user = User(int(message.chat.id))
        if user.is_teacher():
            bot.send_message(message.chat.id, 'Вы успешно подтвердили свои данные. Вы авторизованы!', parse_mode='html')
            bot.send_message(message.chat.id, 'Вот моё главное меню: ', parse_mode='html',
                             reply_markup=teachers_msg.main_menu("name")[0])

        else:
            bot.send_message(message.chat.id, 'Ты успешно подтвердил свои данные. Ты авторизован!', parse_mode='html')
            bot.send_message(message.chat.id, 'Вот моё главное меню: ', parse_mode='html',
                             reply_markup=students_msg.main_menu("name")[0])
    else:
        msg2 = bot.send_message(message.chat.id, check, parse_mode='html', reply_markup=users_msg.student_back())
        bot.register_next_step_handler(msg2, check_password)


# -------------------------------------- ЛИЧНЫЙ КАБИНЕТ --------------------------------------------------
def ask_secret_leader(message):
    chat_id = message.chat.id
    password_l = message.text
    if password_l == 'lider1337':
        account = Account(chat_id)
        account.update_leader()
        msg = 'Верификация пройдена успешно!'
        bot.send_message(chat_id, msg, parse_mode='html', reply_markup=student_lk.lk())
    else:
        bot.send_message(chat_id,
                         'Скорее всего ты неверно ввёл пароль, попробуй ещё раз попозже или напиши в поддержку!',
                         parse_mode='html', reply_markup=users_msg.back_to_lk())

        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def change_username(message):  # устанавливает username
    username = message.text
    chat_id = message.chat.id
    val = validation.validFIO(username)  # проверка валидационная
    if val == 'Всё отлично!':
        account = Account(chat_id)
        account.change_username(username)
        user = User(chat_id)
        bot.send_message(message.chat.id, f'Ваши данные успешно изменены, {user.username()}', parse_mode='html')
        if user.is_teacher():

            bot.send_message(chat_id=message.chat.id,
                             text=teacher_lk.change_account(user.username())[1],
                             parse_mode='html', reply_markup=teacher_lk.change_account(user.username())[0])
        else:

            bot.send_message(chat_id=message.chat.id,
                             text=student_lk.change_account(user.username())[1],
                             reply_markup=student_lk.change_account(user.username())[0], parse_mode='html')

    else:  # если не прошла валидацию, то ещё раз можно ввести
        msg = val
        msg2 = bot.send_message(message.chat.id, msg, parse_mode='html')
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg2, change_username)


def change_password(message):  # устанавливает username
    password = message.text
    chat_id = message.chat.id
    val = validation.validPassword(password)  # проверка валидационная
    if val == 'Всё отлично!':
        account = Account(chat_id)
        account.change_password(password)
        user = User(chat_id)
        bot.send_message(message.chat.id, f'Ваши данные успешно изменены, {user.username()}', parse_mode='html')
        if user.is_teacher():

            bot.send_message(chat_id=message.chat.id,
                             text=teacher_lk.change_account(user.username())[1],
                             parse_mode='html', reply_markup=teacher_lk.change_account(user.username())[0])
        else:

            bot.send_message(chat_id=message.chat.id,
                             text=student_lk.change_account(user.username())[1],
                             reply_markup=student_lk.change_account(user.username())[0], parse_mode='html')

    else:  # если не прошла валидацию, то ещё раз можно ввести
        msg = val
        msg2 = bot.send_message(message.chat.id, msg, parse_mode='html')
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg2, change_password)


# --------------------------- РАСПИСАНИЕ ---------------------------------

def change_cab(message):
    new_cab = message.text
    chat_id = message.chat.id

    user = User(chat_id)

    msg = student_schedule.change_classroom(user.groupe(), new_cab)

    bot.send_message(chat_id=message.chat.id,
                     text=msg[1],
                     reply_markup=msg[0], parse_mode='html')


# -------------------------- ДОМАШНЕЕ ЗАДАНИЕ CОЗДАНИЕ --------------------

def ask_create_hw_topic(message):
    chat_id = message.chat.id
    title = message.text

    hw = Homework(chat_id)
    hw.update_title(title)

    msg = teacher_hw.create_title(title)

    bot.send_message(chat_id, msg[1], parse_mode='html', reply_markup=msg[0])

    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def ask_create_hw_text(message):
    chat_id = message.chat.id
    text = message.text
    hw = Homework(chat_id)
    hw.update_text(text)

    info = hw.get_now_hw_info()

    msg = teacher_hw.homework_content(info['username'], info['groupe'], info['department'], info['title'], info['text'],
                                      info['deadline_d'], info['deadline_t'],
                                      info['file'])  # подробнее в func.py

    if msg[2] == 'не указан':  # тут говориться о файле

        bot.send_message(chat_id, msg[1], reply_markup=msg[0], parse_mode='html')

    else:

        src = '/root/environments/SoftUbot/for_files/' + msg[2]
        doc = open(src, 'rb')
        bot.send_document(message.chat.id, doc, reply_markup=msg[2], caption=msg[0],
                          parse_mode='html')


def ask_deadline_day(message):
    chat_id = message.chat.id
    deadline_d = message.text
    val = validation.validDeadline_date(message.text)
    if val == 'Всё отлично!':
        hw = Homework(chat_id)
        hw.update_deadline_date(deadline_d)

        info = hw.get_now_hw_info()

        msg = teacher_hw.homework_content(info['username'], info['groupe'], info['department'], info['title'],
                                          info['text'],
                                          info['deadline_d'], info['deadline_t'],
                                          info['file'])  # подробнее в func.py

        if msg[2] == 'не указан':  # тут говориться о файле

            bot.send_message(chat_id, msg[1], reply_markup=msg[0], parse_mode='html')

        else:

            src = '/root/environments/SoftUbot/for_files/' + msg[2]
            doc = open(src, 'rb')
            bot.send_document(message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                              parse_mode='html')

    else:
        msg = val
        msg2 = bot.send_message(chat_id, msg, parse_mode='html')
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg2, ask_deadline_day)


def ask_deadline_time(message):
    chat_id = message.chat.id
    deadline_t = message.text
    val = validation.validDeadline_time(message.text)
    if val == 'Всё отлично!':
        hw = Homework(chat_id)
        hw.update_deadline_time(deadline_t)

        info = hw.get_now_hw_info()

        msg = teacher_hw.homework_content(info['username'], info['groupe'], info['department'], info['title'],
                                          info['text'],
                                          info['deadline_d'], info['deadline_t'],
                                          info['file'])  # подробнее в func.py

        if msg[2] == 'не указан':  # тут говориться о файле

            bot.send_message(chat_id, msg[1], reply_markup=msg[0], parse_mode='html')

        else:

            src = '/root/environments/SoftUbot/for_files/' + msg[2]
            doc = open(src, 'rb')
            bot.send_document(message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                              parse_mode='html')

    else:
        msg = val
        msg2 = bot.send_message(chat_id, msg, parse_mode='html')
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg2, ask_deadline_time)


# ---------------------------- ДОМАШНЕЕ ЗАДАНИЕ ИЗМЕНЕНИЕ -----------------
def ask_change_hw_title(message):
    chat_id = message.chat.id
    title = message.text

    hw = ChangeHomework(chat_id)
    hw.update_title(title)

    info = hw.get_hw_info(hw.get_id_hw())

    msg = teacher_hw.homework_change_content(hw.get_id_hw(), info['username'], info['groupe'], info['department'],
                                             info['title'],
                                             info['text'],
                                             info['deadline_d'], info['deadline_t'],
                                             info['file'])  # подробнее в func.py

    if msg[2] == 'не указан':  # тут говориться о файле

        bot.send_message(chat_id, msg[1], reply_markup=msg[0], parse_mode='html')

    else:

        src = '/root/environments/SoftUbot/for_files/' + msg[2]
        doc = open(src, 'rb')
        bot.send_document(message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                          parse_mode='html')

    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def ask_change_hw_text(message):
    chat_id = message.chat.id
    text = message.text
    hw = ChangeHomework(chat_id)
    hw.update_text(text)

    info = hw.get_hw_info(hw.get_id_hw())

    msg = teacher_hw.homework_change_content(hw.get_id_hw(), info['username'], info['groupe'], info['department'],
                                             info['title'],
                                             info['text'],
                                             info['deadline_d'], info['deadline_t'],
                                             info['file'])  # подробнее в func.py

    if msg[2] == 'не указан':  # тут говориться о файле

        bot.send_message(chat_id, msg[1], reply_markup=msg[0], parse_mode='html')

    else:

        src = '/root/environments/SoftUbot/for_files/' + msg[2]
        doc = open(src, 'rb')
        bot.send_document(message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                          parse_mode='html')


def ask_deadline_day_change(message):
    chat_id = message.chat.id
    deadline_d = message.text
    val = validation.validDeadline_date(message.text)
    if val == 'Всё отлично!':
        hw = ChangeHomework(chat_id)
        hw.update_deadline_d(deadline_d)

        info = hw.get_hw_info(hw.get_id_hw())

        msg = teacher_hw.homework_change_content(hw.get_id_hw(), info['username'], info['groupe'], info['department'],
                                                 info['title'], info['text'],
                                                 info['deadline_d'], info['deadline_t'],
                                                 info['file'])  # подробнее в func.py

        if msg[2] == 'не указан':  # тут говориться о файле

            bot.send_message(chat_id, msg[1], reply_markup=msg[0], parse_mode='html')

        else:

            src = '/root/environments/SoftUbot/for_files/' + msg[2]
            doc = open(src, 'rb')
            bot.send_document(message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                              parse_mode='html')

    else:
        msg = val
        msg2 = bot.send_message(chat_id, msg, parse_mode='html')
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg2, ask_deadline_day_change)


def ask_deadline_time_change(message):
    chat_id = message.chat.id
    deadline_t = message.text
    val = validation.validDeadline_time(message.text)
    if val == 'Всё отлично!':
        hw = ChangeHomework(chat_id)
        hw.update_deadline_t(deadline_t)

        info = hw.get_hw_info(hw.get_id_hw())

        msg = teacher_hw.homework_change_content(hw.get_id_hw(), info['username'], info['groupe'], info['department'],
                                                 info['title'],
                                                 info['text'],
                                                 info['deadline_d'], info['deadline_t'],
                                                 info['file'])  # подробнее в func.py

        if msg[2] == 'не указан':  # тут говориться о файле

            bot.send_message(chat_id, msg[1], reply_markup=msg[0], parse_mode='html')

        else:

            src = '/root/environments/SoftUbot/for_files/' + msg[2]
            doc = open(src, 'rb')
            bot.send_document(message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                              parse_mode='html')

    else:
        msg = val
        msg2 = bot.send_message(chat_id, msg, parse_mode='html')
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(msg2, ask_deadline_time_change)


@bot.message_handler(content_types=['document'])
def ask_file(message):
    chat_id = message.chat.id
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        fileName = str(message.document.file_name)

        src = '/root/environments/SoftUbot/for_files/' + fileName
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Файл удачно принят!")

        hw = Homework(chat_id)
        hw.update_file(fileName)

        info = hw.get_now_hw_info()

        msg = teacher_hw.homework_content(info['username'], info['groupe'], info['department'], info['title'],
                                          info['text'],
                                          info['deadline_d'], info['deadline_t'],
                                          info['file'])  # подробнее в func.py

        src = '/root/environments/SoftUbot/for_files/' + msg[2]
        doc = open(src, 'rb')
        bot.send_document(message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                          parse_mode='html')


    except Exception as e:
        bot.reply_to(message, e)
        msg2 = 'Не удалось принять ваш файл! Попробуйте ещё раз позже!'
        bot.send_message(chat_id, msg2, parse_mode='html', reply_markup=teacher_hw.back_to_hw_content())
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def file_change(message):
    chat_id = message.chat.id
    hw = ChangeHomework(chat_id)
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        fileName = str(message.document.file_name)

        src = '/root/environments/SoftUbot/for_files/' + fileName
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Файл удачно принят!")

        hw.update_file(fileName)

        info = hw.get_hw_info(hw.get_id_hw())

        msg = teacher_hw.homework_change_content(hw.get_id_hw(), info['username'], info['groupe'], info['department'],
                                                 info['title'], info['text'],
                                                 info['deadline_d'], info['deadline_t'],
                                                 info['file'])  # подробнее в func.py

        src = '/root/environments/SoftUbot/for_files/' + msg[2]
        doc = open(src, 'rb')
        bot.send_document(message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                          parse_mode='html')


    except Exception as e:
        bot.reply_to(message, e)
        msg2 = 'Не удалось принять ваш файл! Попробуйте ещё раз позже!'
        bot.send_message(chat_id, msg2, parse_mode='html',
                         reply_markup=teacher_hw.back_to_change_hw_content(hw.get_id_hw()))
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


@bot.message_handler(content_types=["location"])
def location(message):
    chat_id = message.chat.id
    # user = User(message.chat.id)

    if message.location is not None:
        # print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        # ------ формула окружности (где числа -  это точка центра окружности), а R -  радиус-------
        # if (message.location.latitude - 55.980234) ** 2 + (
        #         message.location.longitude - 37.578793) ** 2 <= 0.001 * 0.001:
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.send_message(message.chat.id, check.for_location(chat_id)[1], reply_markup=check.for_location(chat_id)[0])
        bot.send_message(message.chat.id, "Всё успешно!", reply_markup=students_msg.back_to_main_menu())
    else:
        bot.send_message(message.chat.id, "Я тебя не могу отметить! Видимо,ты скрываешь свою геолокацию)))",
                         reply_markup=students_msg.back_to_main_menu())


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # ------------ БЛОК РЕГИСТРАЦИИ И АВТОРИЗАЦИИ ---------------------

    # кнопка зарегистрироваться
    if call.data == 'go_login':  # лежит в  users/user_msgr
        msg = users_msg.teacher_or_student()[1]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=users_msg.teacher_or_student()[0], parse_mode='html')
    # кнопка контакты
    if call.data == 'contacts':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=settings.text_help,
                              reply_markup=users_msg.home_back(), parse_mode='html')
    # кнопка "О нас"
    if call.data == 'info_no_reg':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=settings.text_info,
                              reply_markup=users_msg.home_back(), parse_mode='html')

    # кнопка назад в меню с регитсрацией
    if call.data == 'back_home':
        msg = users_msg.home()[1]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=users_msg.home()[0], parse_mode='html')

    if call.data == 'student':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=users_msg.student()[1],
                              reply_markup=users_msg.student()[0], parse_mode='html')

    if call.data == 'back_student':  # возвращает в меню с вопросами Авторизация или Регистрация ?
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        user = RegistrationForm(call.message.chat.id)
        user.delete_user()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=users_msg.student()[1],
                              reply_markup=users_msg.student()[0], parse_mode='html')

    if call.data == 'reg_student':  # спрашивает ФИО
        user = RegistrationForm(call.message.chat.id)  # users/models.py
        if not func_main.new_reg_session(call.message.chat.id):
            user.create_user()  # создаётся новый пользователь

            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Укажи cвои ФИО:', parse_mode='html')  # спрашивает ФИО

            bot.register_next_step_handler(msg, ask_username)  # переносит пользователя в функцию изменения имени
        else:

            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Укажи cвои ФИО:', parse_mode='html')  # спрашивает ФИО

            bot.register_next_step_handler(msg, ask_username)  # переносит пользователя в функцию изменения имени

    if call.data == 'reg_password':  # промежуточная менюшка, спрашивает про установку пароля
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Укажи пароль ', parse_mode='html')  # спрашивает пароль

        bot.register_next_step_handler(msg, ask_password)  # переносит пользователя в функцию изменения пароля

    if call.data == 'reg_groupe':  # вытаскивает 1-ю страницу списка из групп и просит выбрать группу
        msg = users_msg.reg_group(1, settings.groupe_list)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              parse_mode='html', reply_markup=msg[0])

    for i in list(range(10)):  # для i = [0,1,2,3,4]

        if call.data == 'next_page_groupe_{}'.format(i):  # переход на следующую страницу
            msg = users_msg.reg_group(i + 1, settings.groupe_list)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        if call.data == 'back_page_groupe_{}'.format(i):  # переход на предидущую страницу
            msg = users_msg.reg_group(i - 1, settings.groupe_list)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        for x in list(range(10)):  # выбирает группу (x - это номер курса, i -  это номер группы в этом курсе)
            if call.data == 'reg_{}0{}'.format(x, i):
                user = RegistrationForm(call.message.chat.id)
                user.update_groupe(int(f'{x}0{i}'))
                user.move_to_all_in_one()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=users_msg.end_reg(x, i)[1], parse_mode='html')
                bot.send_message(call.message.chat.id, users_msg.end_reg(x, i)[2], parse_mode='html')
                bot.send_message(call.message.chat.id, users_msg.end_reg(x, i)[3],
                                 reply_markup=users_msg.end_reg(x, i)[0],
                                 parse_mode='html')

    if call.data == 'auth_student':
        user = LogInForm(call.message.chat.id)  # users/models.py
        if not func_main.new_auth_session(call.message.chat.id):
            user.create_session()  # создаётся новое подключение

            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Укажи cвои ФИО:', parse_mode='html')  # спрашивает ФИО

            bot.register_next_step_handler(msg, check_username)  # переносит пользователя в функцию проверки имени
        else:
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Укажи cвои ФИО:', parse_mode='html')  # спрашивает ФИО

            bot.register_next_step_handler(msg, check_username)  # переносит пользователя в функцию проверки имени

    if call.data == 'teacher':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=users_msg.teacher()[1],
                              reply_markup=users_msg.teacher()[0], parse_mode='html')

    if call.data == 'auth_teacher':
        user = LogInForm(call.message.chat.id)  # users/models.py
        if not func_main.new_auth_session(call.message.chat.id):
            user.create_session()  # создаётся новое подключение

            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Укажите cвои ФИО:', parse_mode='html')  # спрашивает ФИО

            bot.register_next_step_handler(msg, check_username)  # переносит пользователя в функцию проверки имени
        else:
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Укажите cвои ФИО:', parse_mode='html')  # спрашивает ФИО

            bot.register_next_step_handler(msg, check_username)  # переносит пользователя в функцию проверки имени

    # ---------------------------------------------- ГЛАВНОЕ МЕНЮ -----------------------------------------
    if call.data == 'back_main_menu':
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        user = User(call.message.chat.id)
        if user.is_teacher():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=teachers_msg.main_menu(user.username())[1], parse_mode='html',
                                  reply_markup=teachers_msg.main_menu(user.username())[0])
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=students_msg.main_menu(user.username())[1], parse_mode='html',
                                  reply_markup=students_msg.main_menu(user.username())[0])

    if call.data == 'info':
        user = User(call.message.chat.id)
        if user.is_teacher():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=settings.text_info,
                                  reply_markup=teachers_msg.back_to_main_menu(), parse_mode='html')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=settings.text_info,
                                  reply_markup=students_msg.back_to_main_menu(), parse_mode='html')

    if call.data == 'kabinet':

        user = User(call.message.chat.id)
        if user.is_teacher():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=teacher_lk.lk_teacher()[1],
                                  reply_markup=teacher_lk.lk_teacher()[0], parse_mode='html')
        else:

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=student_lk.lk_student()[1],
                                  reply_markup=student_lk.lk_student()[0], parse_mode='html')

    if call.data == 'check_para':
        bot.send_message(call.message.chat.id, check.send_geo()[1], reply_markup=check.send_geo()[0])

    if call.data == 'checked_me':
        user = User(call.message.chat.id)
        if user.is_teacher():
            msg = attendance.check_groupe(1, settings.groupe_list_2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=msg[1],
                                  reply_markup=msg[0], parse_mode='html')

        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=check.check_me(user.groupe())[1],
                                  reply_markup=check.check_me(user.groupe())[0], parse_mode='html')

    for i in list(range(10)):  # для i = [0,1,2,3,4 ... 9]

        if call.data == 'next_page_groupe_{}_check'.format(i):  # переход на следующую страницу
            msg = attendance.check_groupe(i + 1, settings.groupe_list_2)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        if call.data == 'back_page_groupe_{}_check'.format(i):  # переход на предидущую страницу
            msg = attendance.check_groupe(i - 1, settings.groupe_list_2)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        for x in list(range(10)):  # для i = [0,1,2,3,4 ... 9]
            if call.data == 'check_{}0{}'.format(x, i):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Вот список <b>отметившихся:</b>',
                                      parse_mode='html')

                groupe = int(f'{x}0{i}')

                doc = attendance.table_otmetka(groupe)

                bot.send_document(call.message.chat.id, doc, reply_markup=teachers_msg.back_to_main_menu())

    if call.data == 'schedule':
        user = User(call.message.chat.id)
        if user.is_teacher():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='В будущем <i>преподаватели</i>ds тоже смогут смотреть ДЗ',
                                  reply_markup=teachers_msg.back_to_main_menu(), parse_mode='html')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=student_schedule.schedule_main()[1],
                                  reply_markup=student_schedule.schedule_main()[0], parse_mode='html')

    if call.data == 'home_work':
        user = User(call.message.chat.id)
        if user.is_teacher():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=teacher_hw.homework_main()[1],
                                  reply_markup=teacher_hw.homework_main()[0], parse_mode='html')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=student_hw.homework_main()[1],
                                  reply_markup=student_hw.homework_main()[0], parse_mode='html')

    # ---------------------------------------------- ЛИЧНЫЙ КАБИНЕТ -----------------------------------------------

    if call.data == 'my_information':
        user = User(call.message.chat.id)
        if user.is_teacher():
            msg = teacher_lk.lk(user.get_info())
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=msg[1],
                                  reply_markup=msg[0], parse_mode='html')
        else:
            if user.is_leader():
                msg = student_lk.lk(user.get_info())
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=msg[1],
                                      reply_markup=msg[0], parse_mode='html')
            else:
                msg = student_lk.lk_no_leader(user.get_info())
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=msg[1],
                                      reply_markup=msg[0], parse_mode='html')
    if call.data == 'support':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=settings.text_help,
                              reply_markup=users_msg.back_to_lk(), parse_mode='html')

    if call.data == 'back_lk':
        user = User(call.message.chat.id)
        if user.is_teacher():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=teacher_lk.lk_teacher()[1],
                                  reply_markup=teacher_lk.lk_teacher()[0], parse_mode='html')
        else:

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=student_lk.lk_student()[1],
                                  reply_markup=student_lk.lk_student()[0], parse_mode='html')

    if call.data == 'change_leader':
        user = User(call.message.chat.id)
        msg = "Окей, {}! \nЧто бы стать лидером, нужно ввести секретный пароль:".format(user.username())
        msg2 = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                                     parse_mode='html')
        bot.register_next_step_handler(msg2, ask_secret_leader)

    if call.data == 'change_account':
        user = User(call.message.chat.id)
        if user.is_teacher():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=teacher_lk.change_account(user.username())[1],
                                  parse_mode='html', reply_markup=teacher_lk.change_account(user.username())[0])
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=student_lk.change_account(user.username())[1],
                                  parse_mode='html', reply_markup=student_lk.change_account(user.username())[0])

    if call.data == 'change_name':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Хорошо, укажите новое ФИО:',
                                    parse_mode='html')

        bot.register_next_step_handler(msg, change_username)

    if call.data == 'change_password':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Хорошо, укажите новый пароль:',
                                    parse_mode='html')

        bot.register_next_step_handler(msg, change_password)

    if call.data == 'change_groupe':
        msg = student_lk.change_groupe(1, settings.groupe_list)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              parse_mode='html', reply_markup=msg[0])

    for i in list(range(10)):  # для i = [0,1,2,3,4]

        if call.data == 'next_page_groupe_{}_change'.format(i):  # переход на следующую страницу
            msg = student_lk.change_groupe(i + 1, settings.groupe_list)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        if call.data == 'back_page_groupe_{}_change'.format(i):  # переход на предидущую страницу
            msg = student_lk.change_groupe(i - 1, settings.groupe_list)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        for x in list(range(10)):  # выбирает группу (x - это номер курса, i -  это номер группы в этом курсе)
            if call.data == 'change_{}0{}'.format(x, i):
                account = Account(call.message.chat.id)
                account.change_groupe(int(f'{x}0{i}'))
                user = User(call.message.chat.id)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f'Ваши данные успешно изменены, {user.username()}', parse_mode='html')

                bot.send_message(chat_id=call.message.chat.id,
                                 text=student_lk.change_account(user.username())[1],
                                 reply_markup=student_lk.change_account(user.username())[0], parse_mode='html')

    # ---------------------------------------------- РАСПИСАНИЕ -----------------------------------------------
    if call.data == 'now':
        user = User(call.message.chat.id)
        msg = student_schedule.now(user.groupe(), user.is_leader())

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              reply_markup=msg[0], parse_mode='html')

    if call.data == 'change_cab':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напиши мне № кабинета',
                                    parse_mode='html')
        bot.register_next_step_handler(msg, change_cab)

    if call.data == 'today':
        user = User(call.message.chat.id)
        msg = student_schedule.today(user.groupe())

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              reply_markup=msg[0], parse_mode='html')

    if call.data == 'tomorrow':
        user = User(call.message.chat.id)
        msg = student_schedule.tomorrow(user.groupe())

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              reply_markup=msg[0], parse_mode='html')

    if call.data == 'weak':
        user = User(call.message.chat.id)
        msg = student_schedule.weak(user.groupe())

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              parse_mode='html')

        bot.send_document(call.message.chat.id, msg[2], reply_markup=msg[0])

    if call.data == 'back_schedule':

        user = User(call.message.chat.id)
        if user.is_teacher():
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='В будущем <i>преподаватели</i>ds тоже смогут смотреть ДЗ',
                                  reply_markup=teachers_msg.back_to_main_menu(), parse_mode='html')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=student_schedule.schedule_main()[1],
                                  reply_markup=student_schedule.schedule_main()[0], parse_mode='html')

    if call.data == 'back_schedule_weak':
        bot.send_message(call.message.chat.id, student_schedule.schedule_main()[1],
                         reply_markup=student_schedule.schedule_main()[0])
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)

    # ---------------------------------------------- ДОМАШНЕЕ ЗАДАНИЕ -----------------------------------------------

    if call.data == 'back_hw_teacher':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=teacher_hw.homework_main()[1],
                         reply_markup=teacher_hw.homework_main()[0], parse_mode='html')

    if call.data == 'back_hw_student':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=student_hw.homework_main()[1],
                         reply_markup=student_hw.homework_main()[0], parse_mode='html')

    if call.data == 'create_hw':
        user = User(call.message.chat.id)
        msg = teacher_hw.department_subjects(user.department())

        hw = Homework(call.message.chat.id)
        hw.reset_hw()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              reply_markup=msg[0], parse_mode='html')

    if call.data == 'change_hw':
        user = User(call.message.chat.id)
        department = str(user.department())
        msg = teacher_hw.change_homeworks(department)

        hw = Homework(call.message.chat.id)
        hw.reset_hw()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              reply_markup=msg[0], parse_mode='html')

    if call.data == 'delete_hw':
        user = User(call.message.chat.id)
        department = str(user.department())
        msg = teacher_hw.delete_homeworks(department)

        hw = Homework(call.message.chat.id)
        hw.reset_hw()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              reply_markup=msg[0], parse_mode='html')

    # --------------------------------Создание ДЗ---------------------------------

    for i in settings.subject_list():  # это для выбора предмета (subject)

        if call.data == '{}'.format(i):
            user = User(call.message.chat.id)
            if user.is_teacher():
                hw = Homework(call.message.chat.id)
                hw.update_subject(i)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Отлично, Вы выбрали - <b> {} </b>.\n'
                                           'Выберите группу, для которой предназначено домашнее задание: '.format(i),

                                      parse_mode='html')
                msg = teacher_hw.homework_groupe(1, settings.groupe_list)

                bot.send_message(chat_id=call.message.chat.id, text=msg[1], parse_mode='html', reply_markup=msg[0])

    for i in list(range(10)):  # для i = [0,1,2,3,4]

        if call.data == 'next_page_groupe_{}_hw'.format(i):  # переход на следующую страницу
            msg = teacher_hw.homework_groupe(i + 1, settings.groupe_list)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        if call.data == 'back_page_groupe_{}_hw'.format(i):  # переход на предидущую страницу
            msg = teacher_hw.homework_groupe(i - 1, settings.groupe_list)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        for x in list(range(10)):  # выбирает группу (x - это номер курса, i -  это номер группы в этом курсе)
            if call.data == 'hw_{}0{}'.format(x, i):
                hw = Homework(call.message.chat.id)
                hw.update_groupe(int(f'{x}0{i}'))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f'Вы выбрали<b> {x}0{i} группу.</b>', parse_mode='html')

                msg2 = bot.send_message(chat_id=call.message.chat.id,
                                        text='Окей, напишите <b>заголовок</b> Вашего домашнего задания',
                                        parse_mode='html')

                bot.register_next_step_handler(msg2, ask_create_hw_topic)

    if call.data == 'create_text_hw':
        msg2 = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text='Окей, напишите <b>весь текст</b>, который нужно прикрепить к ДЗ:',
                                     parse_mode='html')

        bot.register_next_step_handler(msg2, ask_create_hw_text)

    if call.data == 'deadline_d':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg2 = bot.send_message(call.message.chat.id, 'Окей, напишите дату дедлайна!', parse_mode='html')
        bot.register_next_step_handler(msg2, ask_deadline_day)

    if call.data == 'deadline_t':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg2 = bot.send_message(call.message.chat.id, 'Окей, напишите время дедлайна!', parse_mode='html')
        bot.register_next_step_handler(msg2, ask_deadline_time)

    if call.data == 'plus_file':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg2 = bot.send_message(call.message.chat.id,
                                'Окей, отправьте мне файл, который нужно прикрепить: ', parse_mode='html')
        bot.register_next_step_handler(msg2, ask_file)

    if call.data == 'back_hw_content':
        hw = Homework(call.message.chat.id)
        info = hw.get_now_hw_info()

        msg = teacher_hw.homework_content(info['username'], info['groupe'], info['department'], info['title'],
                                          info['text'],
                                          info['deadline_d'], info['deadline_t'],
                                          info['file'])  # подробнее в func.py

        if msg[2] == 'не указан':  # тут говориться о файле

            bot.send_message(call.message.chat.id, msg[1], reply_markup=msg[0], parse_mode='html')

        else:

            src = '/root/environments/SoftUbot/for_files/' + msg[2]
            doc = open(src, 'rb')
            bot.send_document(call.message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                              parse_mode='html')

    if call.data == 'confirm':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        hw = Homework(call.message.chat.id)
        hw.move_to_homework_all()
        hw.reset_hw()

        bot.send_message(call.message.chat.id, 'Отлично! Задание успешно отпрвлено!\nГлавное меню:',
                         reply_markup=teachers_msg.back_to_main_menu())

    # ---------------------------Изменение ДЗ ----------------------------------
    for i in list(range(1000)):

        if call.data == 'prepod_delete_{}'.format(i):

            hw = ChangeHomework(call.message.chat.id)
            info = hw.get_hw_info(i)

            msg = teacher_hw.homework_delete_content(i, info['username'], info['groupe'], info['department'],
                                                     info['title'],
                                                     info['text'],
                                                     info['deadline_d'], info['deadline_t'],
                                                     info['file'])  # подробнее в func.py

            hw.save_id_hw(i)  # сохраняем номер выбранного дз

            if msg[2] == 'не указан':  # тут говориться о файле

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=msg[1], reply_markup=msg[0], parse_mode='html')

            else:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                src = '/root/environments/SoftUbot/for_files/' + msg[2]
                doc = open(src, 'rb')
                bot.send_document(call.message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                                  parse_mode='html')

        if call.data == 'prepod_change_{}'.format(i):  # i -  это id_hw в БД
            hw = ChangeHomework(call.message.chat.id)
            info = hw.get_hw_info(i)

            msg = teacher_hw.homework_change_content(i, info['username'], info['groupe'], info['department'],
                                                     info['title'],
                                                     info['text'],
                                                     info['deadline_d'], info['deadline_t'],
                                                     info['file'])  # подробнее в func.py

            hw.save_id_hw(i)  # сохраняем номер выбранного дз

            if msg[2] == 'не указан':  # тут говориться о файле

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=msg[1], reply_markup=msg[0], parse_mode='html')

            else:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                src = '/root/environments/SoftUbot/for_files/' + msg[2]
                doc = open(src, 'rb')
                bot.send_document(call.message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                                  parse_mode='html')

    if call.data == 'title_change':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg2 = bot.send_message(call.message.chat.id, 'Окей, напишите новый заголовок', parse_mode='html')
        bot.register_next_step_handler(msg2, ask_change_hw_title)

    if call.data == 'text_change':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg2 = bot.send_message(call.message.chat.id, 'Окей, напишите новый текст', parse_mode='html')
        bot.register_next_step_handler(msg2, ask_change_hw_text)

    if call.data == 'deadline_d_change':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg2 = bot.send_message(call.message.chat.id, 'Окей, напишите дату дедлайна:', parse_mode='html')
        bot.register_next_step_handler(msg2, ask_deadline_day_change)

    if call.data == 'deadline_t_change':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg2 = bot.send_message(call.message.chat.id, 'Окей, напишите время дедлайна:', parse_mode='html')
        bot.register_next_step_handler(msg2, ask_deadline_time_change)

    if call.data == 'file_change':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg2 = bot.send_message(call.message.chat.id,
                                'Окей, отправьте мне файл, который нужно прикрепить: ', parse_mode='html')
        bot.register_next_step_handler(msg2, file_change)

    if call.data == 'groupe_change':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = teacher_hw.homework_groupe_change(1, settings.groupe_list)

        bot.send_message(chat_id=call.message.chat.id, text=msg[1], parse_mode='html', reply_markup=msg[0])

    for i in list(range(10)):  # для i = [0,1,2,3,4]

        if call.data == 'next_page_groupe_{}_hw_change_'.format(i):  # переход на следующую страницу
            msg = teacher_hw.homework_groupe_change(i + 1, settings.groupe_list)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        if call.data == 'back_page_groupe_{}_hw_change_'.format(i):  # переход на предидущую страницу
            msg = teacher_hw.homework_groupe_change(i - 1, settings.groupe_list)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=msg[0])

        for x in list(range(10)):  # выбирает группу (x - это номер курса, i -  это номер группы в этом курсе)
            if call.data == 'hw_change_{}0{}'.format(x, i):
                bot.delete_message(call.message.chat.id, call.message.message_id)
                hw = ChangeHomework(call.message.chat.id)
                hw.update_groupe(int('{}0{}'.format(x, i)))

                info = hw.get_hw_info(hw.get_id_hw())

                msg = teacher_hw.homework_change_content(hw.get_id_hw(), info['username'], info['groupe'],
                                                         info['department'], info['title'],
                                                         info['text'],
                                                         info['deadline_d'], info['deadline_t'],
                                                         info['file'])  # подробнее в func.py

                if msg[2] == 'не указан':  # тут говориться о файле

                    bot.send_message(call.message.chat.id, msg[1], reply_markup=msg[0], parse_mode='html')

                else:

                    src = '/root/environments/SoftUbot/for_files/' + msg[2]
                    doc = open(src, 'rb')
                    bot.send_document(call.message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                                      parse_mode='html')

    if call.data == 'delete_hw_to_hw_id':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        hw = DeleteHomowork(call.message.chat.id)
        hw.delete_hw()

        bot.send_message(chat_id=call.message.chat.id,
                         text=teacher_hw.homework_main()[1],
                         reply_markup=teacher_hw.homework_main()[0], parse_mode='html')

    # -------------------------- ДОМАШНЯЯ РАБОТА ДЛЯ УЧЕНИКОВ -------------------
    if call.data == 'choose_subject':
        user = User(call.message.chat.id)

        msg = student_hw.groupe_subjects(user.groupe())

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg[1],
                              reply_markup=msg[0], parse_mode='html')

    for i in settings.subject_list():  # это для выбора предмета (subject)

        if call.data == '{}'.format(i):
            user = User(call.message.chat.id)
            if not user.is_teacher():
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Отлично, Вы выбрали - <b> {} </b>.\nВот список дз, по этому предмету:'
                                      .format(i),

                                      parse_mode='html')

                msg = student_hw.view_homework(i)

                bot.send_message(chat_id=call.message.chat.id, text=msg[1], parse_mode='html', reply_markup=msg[0])

    for i in list(range(1000)):

        if call.data == 'student_view_{}'.format(i):  # i -  это id_hw в БД
            hw = StudentHomeworkView(i)
            info = hw.get_hw_info()

            msg = student_hw.homework_view_content(info['username'], info['groupe'], info['department'],
                                                   info['title'],
                                                   info['text'],
                                                   info['deadline_d'], info['deadline_t'],
                                                   info['file'])  # подробнее в func.py

            if msg[2] == 'не указан':  # тут говориться о файле

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=msg[1], reply_markup=msg[0], parse_mode='html')

            else:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                src = '/root/environments/SoftUbot/for_files/' + msg[2]
                doc = open(src, 'rb')
                bot.send_document(call.message.chat.id, doc, reply_markup=msg[0], caption=msg[1],
                                  parse_mode='html')


bot.polling(none_stop=True, interval=0)
