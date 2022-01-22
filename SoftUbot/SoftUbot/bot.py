import telebot
from telebot import types
import TIME as time

from datetime import datetime

import settings
from settings import conn, cursor
import validation

from SoftUbot.users import func_main
from SoftUbot.users.models import User, RegistrationForm, LogInForm, Account
from SoftUbot.teachers.models import Homework
from SoftUbot.users import users_msg

from SoftUbot.students import students_msg
from SoftUbot.students import check
from SoftUbot.students import schedule as student_schedule
from SoftUbot.students import homework as student_hw
from SoftUbot.students import lk as student_lk

from SoftUbot.teachers import teachers_msg
from SoftUbot.teachers import attendance
from SoftUbot.teachers import schedule as teacher_schedule
from SoftUbot.teachers import homework as teacher_hw
from SoftUbot.teachers import lk as teacher_lk

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
        msg2 = bot.send_message(chat_id, msg, parse_mode='html', reply_markup=student_lk.lk())
    else:
        msg2 = bot.send_message(chat_id,
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

    msg = teacher_hw.create_text(info['title'], info['text'], info['deadline_d'], info['deadline_t'], info['file'])  # подробнее в func.py

    if msg[2] == 'не указан':  # тут говориться о файле

        bot.send_message(chat_id, msg[1], reply_markup=msg[0], parse_mode='html')

    else:

        src = '/root/environments/bot/for_files/' + msg[1]
        doc = open(src, 'rb')
        bot.send_document(message.chat.id, doc, reply_markup=msg[2], caption=msg[0],
                          parse_mode='html')


@bot.message_handler(content_types=["location"])
def location(message):
    chat_id = message.chat.id
    user = User(message.chat.id)

    if message.location is not None:
        # print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        # if (message.location.latitude - 55.980234) ** 2 + (
        #         message.location.longitude - 37.578793) ** 2 <= 0.001 * 0.001:  # формула окружности (где числа -  это точка центра окружности), а R -  радиус
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
                                      text=users_msg.end_reg(x, i)[0], parse_mode='html')
                bot.send_message(call.message.chat.id, users_msg.end_reg(x, i)[1], parse_mode='html')

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
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=teacher_hw.homework_main()[1],
                              reply_markup=teacher_hw.homework_main()[0], parse_mode='html')

    if call.data == 'back_hw_student':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
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
        msg = teacher_hw.change_homeworks(user.department())

        bot.send_message(call.message.chat.id, msg[1], parse_mode='html', reply_markup=msg[0])

    if call.data == 'delete_hw':
        user = User(call.message.chat.id)
        msg = teacher_hw.delete_homeworks(user.department())

        bot.send_message(call.message.chat.id, msg[1], parse_mode='html', reply_markup=msg[0])

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


bot.polling(none_stop=True, interval=0)
