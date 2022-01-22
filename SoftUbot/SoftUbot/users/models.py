#
#
# в этом файле храняться все модели

import os, sys
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from SoftUbot.settings import conn, cursor


class User:
    def __init__(self, chatid):
        self.chatid = chatid

    def get_info(self):
        result = {}

        cursor.execute("SELECT username FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        username = [item[0] for item in cursor.fetchall()]
        conn.commit()
        result['username'] = username[0]

        cursor.execute("SELECT password FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        password = [item[0] for item in cursor.fetchall()]
        conn.commit()
        result['password'] = password[0]

        cursor.execute("SELECT groupe FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        groupe = [item[0] for item in cursor.fetchall()]
        conn.commit()
        result['groupe'] = groupe[0]

        cursor.execute("SELECT department FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        department = [item[0] for item in cursor.fetchall()]
        conn.commit()
        result['department'] = department[0]

        cursor.execute("SELECT is_teacher FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        is_teacher = [item[0] for item in cursor.fetchall()]
        conn.commit()
        if is_teacher[0] == True:
            status = 'Преподаватель'
        else:
            status = 'Студент'

        result['status'] = status

        cursor.execute("SELECT is_leader FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        is_lider = [item[0] for item in cursor.fetchall()]
        conn.commit()
        result['is_lider'] = is_lider[0]

        return result

    def username(self):
        cursor.execute("SELECT username FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        username = [item[0] for item in cursor.fetchall()]
        conn.commit()

        return username[0]

    def groupe(self):
        cursor.execute("SELECT groupe FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        groupe = [item[0] for item in cursor.fetchall()]
        conn.commit()

        return groupe[0]

    def department(self):
        cursor.execute("SELECT department FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        department = [item[0] for item in cursor.fetchall()]
        conn.commit()

        return department[0]

    def is_teacher(self):
        cursor.execute("SELECT is_teacher FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        is_teacher = [item[0] for item in cursor.fetchall()]
        conn.commit()

        return is_teacher[0]

    def is_leader(self):
        cursor.execute("SELECT is_leader FROM all_in_one WHERE id_telegram = {}".format(self.chatid))
        is_leader = [item[0] for item in cursor.fetchall()]
        conn.commit()

        return is_leader[0]


# user = User(323739054)
# print(user.is_teacher())

class RegistrationForm:
    def __init__(self, chatid):
        self.chatid = chatid

    def create_user(self):
        cursor.execute("insert into telebot_reg values ({}, NULL, NULL, NULL)".format(self.chatid))
        conn.commit()

    def delete_user(self):
        cursor.execute("DELETE FROM telebot_reg WHERE chatid = {}".format(self.chatid))
        conn.commit()

    def update_username(self, username):
        cursor.execute("UPDATE telebot_reg SET username = '{}' where chatid = {}".format(username, self.chatid))
        conn.commit()

    def update_password(self, password):
        cursor.execute("UPDATE telebot_reg SET password = '{}' where chatid = {}".format(password, self.chatid))
        conn.commit()

    def update_groupe(self, groupe):
        cursor.execute("UPDATE telebot_reg SET groupe = '{}' where chatid = {}".format(groupe, self.chatid))
        conn.commit()

    def move_to_all_in_one(self):
        cursor.execute(
            "INSERT INTO all_in_one (username, password, groupe, id_telegram) SELECT username, password, groupe, chatid  FROM telebot_reg WHERE chatid = {};".format(
                self.chatid))
        conn.commit()


class LogInForm:
    def __init__(self, chatid):
        self.chatid = chatid

    def create_session(self):
        cursor.execute("insert into telebot_auth values ({}, NULL, NULL)".format(self.chatid))
        conn.commit()

    def update_username(self, username):
        cursor.execute("UPDATE telebot_auth SET username = '{}' where chatid = {}".format(username, self.chatid))
        conn.commit()

    def update_password(self, password):
        cursor.execute("UPDATE telebot_auth SET password = '{}' where chatid = {}".format(password, self.chatid))
        conn.commit()

    def move_to_all_in_one(self):
        cursor.execute(
            "UPDATE all_in_one SET id_telegram = {} WHERE username = (SELECT username FROM telebot_auth WHERE chatid = {})".format(
                self.chatid, self.chatid))
        conn.commit()


# login = LogInForm(323739054)
# login.move_to_all_in_one()

class Account:
    def __init__(self, chatid):
        self.chatid = chatid

    def change_username(self, username):
        cursor.execute("UPDATE all_in_one SET username = '{}' where id_telegram = {}".format(username, self.chatid))
        conn.commit()

    def change_password(self, password):
        cursor.execute("UPDATE all_in_one SET password = '{}' where id_telegram = {}".format(password, self.chatid))
        conn.commit()

    def change_groupe(self, groupe):
        cursor.execute("UPDATE all_in_one SET groupe = '{}' where id_telegram = {}".format(groupe, self.chatid))
        conn.commit()

    def change_department(self, department):
        cursor.execute("UPDATE all_in_one SET department = '{}' where id_telegram = {}".format(department, self.chatid))
        conn.commit()

    def update_leader(self):
        cursor.execute("UPDATE all_in_one SET is_leader = TRUE where id_telegram = {}".format(self.chatid))
        conn.commit()