import os, sys
from os.path import dirname, join, abspath
from datetime import timedelta, datetime

MSK = timedelta(hours=3)

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from SoftUbot.settings import conn, cursor


class Homework:
    def __init__(self, chatid):
        self.chatid = chatid

    def reset_hw(self):
        cursor.execute("UPDATE homework_bot SET subject = NULL WHERE chatid = {} ".format(self.chatid))
        conn.commit()

        cursor.execute("UPDATE homework_bot SET title = NULL WHERE chatid = {} ".format(self.chatid))
        conn.commit()

        cursor.execute("UPDATE homework_bot SET text_hw = NULL WHERE chatid = {} ".format(self.chatid))
        conn.commit()

        cursor.execute("UPDATE homework_bot SET groupe = NULL WHERE chatid = {} ".format(self.chatid))
        conn.commit()

        cursor.execute("UPDATE homework_bot SET filename = NULL WHERE chatid = {} ".format(self.chatid))
        conn.commit()

        cursor.execute("UPDATE homework_bot SET deadlinedate = NULL WHERE chatid = {} ".format(self.chatid))
        conn.commit()

        cursor.execute("UPDATE homework_bot SET deadlinetime = NULL WHERE chatid = {} ".format(self.chatid))
        conn.commit()

        cursor.execute(
            "UPDATE homework_bot SET pub_date = '{}' WHERE chatid = {} ".format(datetime.now() + MSK, self.chatid))
        conn.commit()

        cursor.execute("UPDATE homework_bot SET id_hw = NULL WHERE chatid = {} ".format(self.chatid))
        conn.commit()

    def update_subject(self, subject):
        cursor.execute("UPDATE homework_bot SET subject = '{}' WHERE chatid = {}".format(subject, self.chatid))
        conn.commit()

    def update_groupe(self, groupe):
        cursor.execute("UPDATE homework_bot SET groupe = {} WHERE chatid = {} ".format(groupe, self.chatid))
        conn.commit()

    def update_title(self, title):
        cursor.execute("UPDATE homework_bot SET title = '{}' WHERE chatid = {} ".format(title, self.chatid))
        conn.commit()

    def update_text(self, text):
        cursor.execute("UPDATE homework_bot SET text_hw = '{}' WHERE chatid = {} ".format(text, self.chatid))
        conn.commit()

    def update_file(self, file):
        cursor.execute("UPDATE homework_bot SET filename = '{}' WHERE chatid = {} ".format(file, self.chatid))
        conn.commit()

    def update_deadline_date(self, deadline_date):
        cursor.execute("UPDATE homework_bot SET deadlinedate = '{}' WHERE chatid = {} ".format(deadline_date,
                                                                                               self.chatid))
        conn.commit()

    def update_deadline_time(self, deadline_time):
        cursor.execute(
            "UPDATE homework_bot SET deadlinetime = '{}' WHERE chatid = {} ".format(deadline_time, self.chatid))
        conn.commit()

    def get_now_hw_info(self):
        info = {}

        # вытаскивает ФИО по chatid:
        cursor.execute("SELECT username FROM homework_bot WHERE chatid ={}".format(self.chatid))
        username = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['username'] = username

        # вытаскивает Кафедру по chatid:
        cursor.execute("SELECT department FROM homework_bot WHERE chatid ={}".format(self.chatid))
        department = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['department'] = department

        # вытаскивает Заголовок по chatid:
        cursor.execute("SELECT subject FROM homework_bot WHERE chatid ={}".format(self.chatid))
        subject = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['subject'] = subject

        # вытаскивает группу, для которой ДЗ, по chatid:
        cursor.execute("SELECT groupe FROM homework_bot WHERE chatid ={}".format(self.chatid))
        groupe = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['groupe'] = groupe

        # вытаскивает Заголовок по chatid:
        cursor.execute("SELECT title FROM homework_bot WHERE chatid ={}".format(self.chatid))
        title = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['title'] = title

        # вытаскивает Текст по chatid:
        cursor.execute("SELECT text_hw FROM homework_bot WHERE chatid ={}".format(self.chatid))
        text = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['text'] = text

        # вытаскивает файл по chatid:
        cursor.execute("SELECT filename FROM homework_bot WHERE chatid ={}".format(self.chatid))
        filename = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        if filename is None:
            info['file'] = 'не указан'
        else:
            info['file'] = filename

        # вытаскивает Дедлайн Дату по id_hw:
        cursor.execute("SELECT deadlinedate FROM homework_bot WHERE chatid ={}".format(self.chatid))
        deadline_d = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        if deadline_d is None:
            info['deadline_d'] = 'не указано'
        else:
            info['deadline_d'] = deadline_d

        # вытаскивает Дедлайн Время по id_hw:
        cursor.execute("SELECT deadlinetime FROM homework_bot WHERE chatid ={}".format(self.chatid))
        deadline_t = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        if deadline_t is None:
            info['deadline_t'] = 'не указано'
        else:
            info['deadline_t'] = deadline_t

        return info

    def move_to_homework_all(self):
        cursor.execute(
            "INSERT INTO homework_all (telegram_id, username, department, subject, groupe, title, text_hw, filename, deadlinedate, deadlinetime, pub_date) SELECT chatid, username, department, subject, groupe, title, text_hw, filename, deadlinedate, deadlinetime, pub_date  FROM homework_bot WHERE chatid = {}".format(
                self.chatid))
        conn.commit()


# print(datetime.now())

# hw = Homework(323739054)
# print(hw.move_to_homework_all())


class ChangeHomework:
    def __init__(self, chatid):
        self.chatid = chatid

    def get_hw_info(self, id_hw):
        info = {}

        # вытаскивает ФИО по chatid:
        cursor.execute("SELECT username FROM homework_all WHERE id_hw ={}".format(id_hw))
        username = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['username'] = username

        # вытаскивает Кафедру по chatid:
        cursor.execute("SELECT department FROM homework_all WHERE id_hw ={}".format(id_hw))
        department = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['department'] = department

        # вытаскивает Заголовок по chatid:
        cursor.execute("SELECT subject FROM homework_all WHERE id_hw ={}".format(id_hw))
        subject = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['subject'] = subject

        # вытаскивает группу, для которой ДЗ, по chatid:
        cursor.execute("SELECT groupe FROM homework_all WHERE id_hw ={}".format(id_hw))
        groupe = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['groupe'] = groupe

        # вытаскивает Заголовок по chatid:
        cursor.execute("SELECT title FROM homework_all WHERE id_hw ={}".format(id_hw))
        title = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['title'] = title

        # вытаскивает Текст по chatid:
        cursor.execute("SELECT text_hw FROM homework_all WHERE id_hw ={}".format(id_hw))
        text = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['text'] = text

        # вытаскивает файл по chatid:
        cursor.execute("SELECT filename FROM homework_all WHERE id_hw ={}".format(id_hw))
        filename = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        if filename is None:
            info['file'] = 'не указан'
        else:
            info['file'] = filename

        # вытаскивает Дедлайн Дату по id_hw:
        cursor.execute("SELECT deadlinedate FROM homework_all WHERE id_hw ={}".format(id_hw))
        deadline_d = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        if deadline_d is None:
            info['deadline_d'] = 'не указано'
        else:
            info['deadline_d'] = deadline_d

        # вытаскивает Дедлайн Время по id_hw:
        cursor.execute("SELECT deadlinetime FROM homework_all WHERE id_hw ={}".format(id_hw))
        deadline_t = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        if deadline_t is None:
            info['deadline_t'] = 'не указано'
        else:
            info['deadline_t'] = deadline_t

        return info

    def save_id_hw(self, id_hw):
        cursor.execute("UPDATE homework_bot SET id_hw = {} WHERE chatid = {} ".format(id_hw, self.chatid))
        conn.commit()

    def get_id_hw(self):
        cursor.execute("SELECT id_hw FROM homework_bot WHERE chatid = {} ".format(self.chatid))
        id_hw = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        return id_hw

    def update_title(self, title):
        cursor.execute("SELECT id_hw FROM homework_bot WHERE chatid = {} ".format(self.chatid))
        id_hw = [item[0] for item in cursor.fetchall()][0]
        conn.commit()

        cursor.execute("UPDATE homework_all SET title = '{}' WHERE id_hw = {} ".format(title, id_hw))
        conn.commit()

    def update_text(self, text):
        cursor.execute("SELECT id_hw FROM homework_bot WHERE chatid = {} ".format(self.chatid))
        id_hw = [item[0] for item in cursor.fetchall()][0]
        conn.commit()

        cursor.execute("UPDATE homework_all SET text_hw = '{}' WHERE id_hw = {} ".format(text, id_hw))
        conn.commit()

    def update_groupe(self, groupe):
        cursor.execute("SELECT id_hw FROM homework_bot WHERE chatid = {} ".format(self.chatid))
        id_hw = [item[0] for item in cursor.fetchall()][0]
        conn.commit()

        cursor.execute("UPDATE homework_all SET groupe = {} WHERE id_hw = {} ".format(groupe, id_hw))
        conn.commit()

    def update_file(self, file):
        cursor.execute("SELECT id_hw FROM homework_bot WHERE chatid = {} ".format(self.chatid))
        id_hw = [item[0] for item in cursor.fetchall()][0]
        conn.commit()

        cursor.execute("UPDATE homework_all SET filename = '{}' WHERE id_hw = {} ".format(file, id_hw))
        conn.commit()

    def update_deadline_d(self, deadline_d):
        cursor.execute("SELECT id_hw FROM homework_bot WHERE chatid = {} ".format(self.chatid))
        id_hw = [item[0] for item in cursor.fetchall()][0]
        conn.commit()

        cursor.execute("UPDATE homework_all SET deadlinedate = '{}' WHERE id_hw = {} ".format(deadline_d, id_hw))
        conn.commit()

    def update_deadline_t(self, deadline_t):
        cursor.execute("SELECT id_hw FROM homework_bot WHERE chatid = {} ".format(self.chatid))
        id_hw = [item[0] for item in cursor.fetchall()][0]
        conn.commit()

        cursor.execute("UPDATE homework_all SET deadlinetime = '{}' WHERE id_hw = {} ".format(deadline_t, id_hw))
        conn.commit()


class DeleteHomowork:
    def __init__(self, chatid):
        self.chatid = chatid

    def delete_hw(self):
        cursor.execute("SELECT id_hw FROM homework_bot WHERE chatid = {} ".format(self.chatid))
        id_hw = [item[0] for item in cursor.fetchall()][0]
        conn.commit()

        cursor.execute("DELETE FROM homework_all WHERE id_hw = {}".format(id_hw))
        conn.commit()
