#
#
# в этом файле храняться все функции

import os, sys

from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from SoftUbot.settings import conn, cursor


# --------------- если пользователь не в системе, то сразу отправляет на регистрацию-------
def new_session(chatid):
    cursor.execute("SELECT * FROM all_in_one WHERE id_telegram = {}".format(chatid))
    reg = cursor.fetchone()
    conn.commit()
    if reg is None:
        return False  # выводит если пользователя нет в системе
    else:
        return True  # выводит если пользователь есть в системе


def new_reg_session(chatid):
    cursor.execute("SELECT * FROM telebot_reg WHERE chatid = {}".format(chatid))
    reg = cursor.fetchone()
    conn.commit()
    if reg is None:
        return False  # выводит если пользователя нет в системе
    else:
        return True  # выводит если пользователь есть в


def new_auth_session(chatid):
    cursor.execute("SELECT * FROM telebot_auth WHERE chatid = {}".format(chatid))
    auth = cursor.fetchone()
    conn.commit()
    if auth is None:
        return False  # выводит если пользователя нет в системе
    else:
        return True  # выводит если пользователь есть в системе


# --------------- функция, которая проверяет полностью ли прошла регистрация-------
def check_all_attr(chatid):
    cursor.execute("SELECT COUNT (*) FROM all_in_one WHERE id_telegram = {}".format(chatid))
    count_chatid = [item[0] for item in cursor.fetchall()]
    conn.commit()
    # print(count_chatid[0])

    if count_chatid[0] == 1:

        cursor.execute("SELECT username FROM all_in_one WHERE id_telegram = {}".format(chatid))
        username = [item[0] for item in cursor.fetchall()]
        # print(username[0])
        conn.commit()

        cursor.execute("SELECT password FROM all_in_one WHERE id_telegram = {}".format(chatid))
        password = [item[0] for item in cursor.fetchall()]
        # print(password[0])
        conn.commit()

        cursor.execute("SELECT groupe FROM all_in_one WHERE id_telegram = {}".format(chatid))
        groupe = [item[0] for item in cursor.fetchall()]
        # print(groupe[0])
        conn.commit()

        try:
            if username[0] is None or password[0] is None or groupe[0] is None:
                return False
            else:
                return True  # значит всё заполнено
        except:
            return False

    else:
        return False


# print(check_all_attr(323739054))

def check_username(username):
    cursor.execute("SELECT COUNT (*) FROM all_in_one WHERE username = '{}'".format(username))
    count_username = [item[0] for item in cursor.fetchall()]
    conn.commit()

    print(count_username[0])
    if count_username[0] == 1:
        return 'Всё отлично!'
    else:
        return 'Ваши ФИО не зарегистрированны!'


def check_password(chatid, password):
    cursor.execute("SELECT username FROM telebot_auth WHERE chatid = {} ".format(chatid))
    username = cursor.fetchone()[0]
    conn.commit()

    cursor.execute(
        "SELECT COUNT (*) FROM all_in_one WHERE username = '{}' AND password = '{}'".format(username, password))
    count = cursor.fetchone()[0]
    conn.commit()

    if count == 1:
        return 'Всё отлично!'
    else:
        return 'Ваш пароль указан не верно'
