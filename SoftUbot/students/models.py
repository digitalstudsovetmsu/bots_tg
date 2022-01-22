import os, sys
from os.path import dirname, join, abspath
from datetime import timedelta, datetime

MSK = timedelta(hours=3)

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from SoftUbot.settings import conn, cursor


class StudentHomeworkView:

    def __init__(self, id_hw):
        self.id_hw = id_hw

    def get_hw_info(self):
        info = {}

        # вытаскивает ФИО по chatid:
        cursor.execute("SELECT username FROM homework_all WHERE id_hw ={}".format(self.id_hw))
        username = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['username'] = username

        # вытаскивает Кафедру по chatid:
        cursor.execute("SELECT department FROM homework_all WHERE id_hw ={}".format(self.id_hw))
        department = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['department'] = department

        # вытаскивает Заголовок по chatid:
        cursor.execute("SELECT subject FROM homework_all WHERE id_hw ={}".format(self.id_hw))
        subject = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['subject'] = subject

        # вытаскивает группу, для которой ДЗ, по chatid:
        cursor.execute("SELECT groupe FROM homework_all WHERE id_hw ={}".format(self.id_hw))
        groupe = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['groupe'] = groupe

        # вытаскивает Заголовок по chatid:
        cursor.execute("SELECT title FROM homework_all WHERE id_hw ={}".format(self.id_hw))
        title = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['title'] = title

        # вытаскивает Текст по chatid:
        cursor.execute("SELECT text_hw FROM homework_all WHERE id_hw ={}".format(self.id_hw))
        text = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        info['text'] = text

        # вытаскивает файл по chatid:
        cursor.execute("SELECT filename FROM homework_all WHERE id_hw ={}".format(self.id_hw))
        filename = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        if filename is None:
            info['file'] = 'не указан'
        else:
            info['file'] = filename

        # вытаскивает Дедлайн Дату по id_hw:
        cursor.execute("SELECT deadlinedate FROM homework_all WHERE id_hw ={}".format(self.id_hw))
        deadline_d = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        if deadline_d is None:
            info['deadline_d'] = 'не указано'
        else:
            info['deadline_d'] = deadline_d

        # вытаскивает Дедлайн Время по id_hw:
        cursor.execute("SELECT deadlinetime FROM homework_all WHERE id_hw ={}".format(self.id_hw))
        deadline_t = [item[0] for item in cursor.fetchall()][0]
        conn.commit()
        if deadline_t is None:
            info['deadline_t'] = 'не указано'
        else:
            info['deadline_t'] = deadline_t

        return info