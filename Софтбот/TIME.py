from datetime import timedelta, datetime
import psycopg2

# подключаем БД
conn = psycopg2.connect(dbname='', user='',
                        password='', host='')
cursor = conn.cursor()  # обращаться будем через курсор


# --------------------------------------ДЛЯ РАСПИСАНИЯ НА СЕГОДНЯ-----------------------------------------------

#  Функция примает в параметры: время сейчас, номер группы
#  возвращает все пары за этот день у этой группы из sql
# чтобы обратиться к функции НЕОБХОДИМО передать параметр "сейчас", он выгладит вот так - datetime.now()
# ПРИМЕР ИСПОЛЬЗОВАНИЯ ФУНКЦИИ: print(schedule_today(datetime.now(), 101))

def schedule_today(time, groupe):
    # вытаскиваем из времени номер дня (сегодняшнего)
    today = time.strftime('%d')

    # меняем тип, что б уж наверняка
    today = int(today)
    # находим номер курса, как первое число в группе
    course = str(groupe)[0]

    # буду использовать срезы (limit) в sql поэтому определим формулу для нахождения первого элемента в каждом дне
    day = 1 + (today - 1) * 6

    # вытаскиваем список названий предметов за этот день
    cursor.execute("SELECT column_{}_p FROM course{} LIMIT 5 OFFSET {}".format(groupe, course, day))
    name = [item[0] for item in cursor.fetchall()]
    conn.commit()

    # вытаскиваем список преподавателей за этот день
    cursor.execute("SELECT column_{}_t FROM course{} LIMIT 5 OFFSET {}".format(groupe, course, day))
    teacher = [item[0] for item in cursor.fetchall()]
    conn.commit()

    # вытаскиваем список кабинетов для пар за этот день
    cursor.execute("SELECT column_{}_k FROM course{} LIMIT 5 OFFSET {}".format(groupe, course, day))
    cab = [item[0] for item in cursor.fetchall()]
    conn.commit()

    # группируем списки по парам (каждая пара -  это словарь)

    para_1 = {'name': name[0], 'teacher': teacher[0], 'cab': cab[0]}
    para_2 = {'name': name[1], 'teacher': teacher[1], 'cab': cab[1]}
    para_3 = {'name': name[2], 'teacher': teacher[2], 'cab': cab[2]}
    para_4 = {'name': name[3], 'teacher': teacher[3], 'cab': cab[3]}
    para_5 = {'name': name[4], 'teacher': teacher[4], 'cab': cab[4]}

    # создаём один единый словарь для всех пар этого дня

    all_pars = {'para_1': para_1, 'para_2': para_2, 'para_3': para_3, 'para_4': para_4, 'para_5': para_5}

    return all_pars  # возвращает этот словарь


# --------------------------------------ДЛЯ РАСПИСАНИЯ НА ЗАВТРА-----------------------------------------------

#  Функция примает в параметры: время сейчас, номер группы
#  возвращает все пары за следущий день у этой группы из sql
# чтобы обратиться к функции НЕОБХОДИМО передать параметр "сейчас", он выгладит вот так - datetime.now()
# ПРИМЕР ИСПОЛЬЗОВАНИЯ ФУНКЦИИ: print(schedule_tomorrow(datetime.now(), 101))

def schedule_tomorrow(time, groupe):
    # вытаскиваем из времени номер дня (сегодняшнего)
    today = time.strftime('%d')
    # меняем тип, что б уж наверняка и добавляем к нашей дате один день
    tomorrow = int(today) + 1
    # находим номер курса, как первое число в группе
    course = str(groupe)[0]

    # буду использовать срезы (limit) в sql поэтому определим формулу для нахождения первого элемента в каждом дне
    day = 1 + (tomorrow - 1) * 6

    # вытаскиваем список названий предметов за этот день
    cursor.execute("SELECT column_{}_p FROM course{} LIMIT 5 OFFSET {}".format(groupe, course, day))
    name = [item[0] for item in cursor.fetchall()]
    conn.commit()

    # вытаскиваем список преподавателей за этот день
    cursor.execute("SELECT column_{}_t FROM course{} LIMIT 5 OFFSET {}".format(groupe, course, day))
    teacher = [item[0] for item in cursor.fetchall()]
    conn.commit()

    # вытаскиваем список кабинетов для пар за этот день
    cursor.execute("SELECT column_{}_k FROM course{} LIMIT 5 OFFSET {}".format(groupe, course, day))
    cab = [item[0] for item in cursor.fetchall()]
    conn.commit()

    # группируем списки по парам (каждая пара -  это словарь)

    para_1 = {'name': name[0], 'teacher': teacher[0], 'cab': cab[0]}
    para_2 = {'name': name[1], 'teacher': teacher[1], 'cab': cab[1]}
    para_3 = {'name': name[2], 'teacher': teacher[2], 'cab': cab[2]}
    para_4 = {'name': name[3], 'teacher': teacher[3], 'cab': cab[3]}
    para_5 = {'name': name[4], 'teacher': teacher[4], 'cab': cab[4]}

    # создаём один единый словарь для всех пар этого дня

    all_pars = {'para_1': para_1, 'para_2': para_2, 'para_3': para_3, 'para_4': para_4, 'para_5': para_5}

    return all_pars


# --------------------------------------ДЛЯ РАСПИСАНИЯ НА СЕЙЧАС-----------------------------------------------

#  Функция примает в параметры: время сейчас, номер группы
#  возвращает пару, которая проходит у этой группы в данный момент времени
# чтобы обратиться к функции НЕОБХОДИМО передать параметр "сейчас", он выгладит вот так - datetime.now()
# ПРИМЕР ИСПОЛЬЗОВАНИЯ ФУНКЦИИ: print(schedule_now(datetime.now(), 101))

def schedule_now(time, groupe):
    today_time = time.strftime(("%H:%M"))  # забирает минуты и часы из времени(которое передано)
    d = int(time.strftime("%d"))  # вытаскивает день
    m = int(time.strftime("%m"))  # вытаскивает месяц

    # ----------------промежуток до первой пары (c 00:00 по 8:59)-------------

    if today_time >= datetime(2020, m, d, 00, 00).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 8,
                                                                                                 59).strftime(
        ("%H:%M")):
        para = {'name': 'Время до первой пары', 'teacher': '---',
                'cab': '---'}  # устанавливаем вот такой параметр для пары
        now_para = False  # параметр, который показывает, что сейчас пара не идёт

    # ---------------------промежуток первой пары (с 9:00 по 10:30)------------
    if today_time >= datetime(2020, m, d, 9, 00).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 10,
                                                                                                30).strftime(("%H:%M")):
        now_para = True  # параметр, который показывает, что сейчас идёт пара
        day = schedule_today(time, groupe)
        para = day['para_1']

    # ---------------промежуток после первой пары до второй пары (c 10:30 по 10:39)-------------
    if today_time >= datetime(2020, m, d, 10, 30).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 10,
                                                                                                 39).strftime(
        ("%H:%M")):
        now_para = False
        para = {'name': 'Перемна между первой и второй парой', 'teacher': '---', 'cab': '---'}

    # -------------------промежуток второй пары (с 10:40 по 12:10)---------------
    if today_time >= datetime(2020, m, d, 10, 40).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 12,
                                                                                                 10).strftime(
        ("%H:%M")):
        now_para = True  # параметр, который показывает, что сейчас идёт пара
        day = schedule_today(time, groupe)
        para = day['para_2']

    # -------------------промежуток большой перемены (с 12:11 по 12:50) ---------------
    if today_time >= datetime(2020, m, d, 12, 11).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 12,
                                                                                                 49).strftime(
        ("%H:%M")):
        now_para = False
        para = {'name': 'Большая Перемна между второй и третей парой', 'teacher': '---', 'cab': '---'}

    # -------------------промежуток третьей пары (с 12:50 по 14:20)---------------
    if today_time >= datetime(2020, m, d, 12, 50).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 14,
                                                                                                 20).strftime(
        ("%H:%M")):
        now_para = True
        day = schedule_today(time, groupe)
        para = day['para_3']

    # ---------------промежуток после третьей пары до четвёртой пары (c 14:21 по 14:29)-------------
    if today_time >= datetime(2020, m, d, 14, 21).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 14,
                                                                                                 29).strftime(
        ("%H:%M")):
        now_para = False
        para = {'name': 'Перемна между третей и четвёртой парой', 'teacher': '---', 'cab': '---'}

    # -------------------промежуток четвёртой пары (с 14:30 по 16:00)---------------
    if today_time >= datetime(2020, m, d, 14, 30).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 16,
                                                                                                 00).strftime(
        ("%H:%M")):
        now_para = True
        day = schedule_today(time, groupe)
        para = day['para_4']

    # ---------------промежуток после четвёртой пары до пятой пары (c 16:01 по 16:09)-------------
    if today_time >= datetime(2020, m, d, 16, 1).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 16,
                                                                                                9).strftime(("%H:%M")):
        now_para = False
        para = {'name': 'Перемна между четвёртой и пятой парой', 'teacher': '---', 'cab': '---'}

    # -------------------промежуток пятой пары (с 16:10 по 17:40)---------------

    if today_time >= datetime(2020, m, d, 16, 10).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 17,
                                                                                                 40).strftime(
        ("%H:%M")):
        now_para = True
        day = schedule_today(time, groupe)
        para = day['para_5']

    # ---------------промежуток после пятой пары (c 17:41 по 23:59)-------------

    if today_time >= datetime(2020, m, d, 17, 41).strftime(("%H:%M")) and today_time <= datetime(2020, m, d, 23,
                                                                                                 59).strftime(
        ("%H:%M")):
        now_para = False
        para = {'name': 'Время после пар', 'teacher': '---', 'cab': '---'}

    # возвращает пару на сегодняшний момент и значение "есть ли пара сейчас"
    return para, now_para


def number_para(time):
    today_time = time.strftime(("%H:%M"))  # забирает минуты и часы из времени(которое передано)
    d = int(time.strftime("%d"))  # вытаскивает день
    m = int(time.strftime("%m"))  # вытаскивает месяц

    # промежуток до первой пары
    if datetime(2020, m, d, 00, 00).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 8,
                                                                                  59).strftime(
        ("%H:%M")):
        para = 0

    # промежуток первой пары
    if datetime(2020, m, d, 9, 00).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 10,
                                                                                 30).strftime(("%H:%M")):
        para = 1

    # промежуток после первой пары до второй пары
    if datetime(2020, m, d, 10, 30).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 10,
                                                                                  39).strftime(
        ("%H:%M")):
        para = 0

    if datetime(2020, m, d, 10, 40).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 12,
                                                                                  10).strftime(
        ("%H:%M")):
        para = 2

    if datetime(2020, m, d, 12, 11).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 12,
                                                                                  49).strftime(
        ("%H:%M")):
        para = 0

    if datetime(2020, m, d, 12, 50).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 14,
                                                                                  20).strftime(
        ("%H:%M")):
        para = 3

    if datetime(2020, m, d, 14, 21).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 14,
                                                                                  29).strftime(
        ("%H:%M")):
        para = 0

    if datetime(2020, m, d, 14, 30).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 16,
                                                                                  00).strftime(
        ("%H:%M")):
        para = 4

    if datetime(2020, m, d, 16, 1).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 16,
                                                                                 9).strftime(("%H:%M")):
        para = 0

    if datetime(2020, m, d, 16, 10).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 17,
                                                                                  40).strftime(
        ("%H:%M")):
        para = 5

    if datetime(2020, m, d, 17, 41).strftime(("%H:%M")) <= today_time <= datetime(2020, m, d, 23,
                                                                                  59).strftime(
        ("%H:%M")):
        para = 0

    return para


def change_classroom(groupe, cab):
    # вытаскиваем из времени номер дня (сегодняшнего)
    today = datetime.now().strftime('%d')
    # меняем тип, что б уж наверняка и добавляем к нашей дате один день
    today = int(today)
    # находим номер курса, как первое число в группе
    course = str(groupe)[0]

    # буду использовать срезы (limit) в sql поэтому определим формулу для нахождения первого элемента в каждом дне
    day = 1 + (today - 1) * 6

    # Limit начинается с 0, а id с 1, поэтому вычитаем эту 1
    number = number_para(datetime.now()) + day - 1

    cursor.execute("SELECT id FROM course{} ORDER BY id LIMIT 1 OFFSET {}".format(course, number))
    id = int(([item[0] for item in cursor.fetchall()])[0])
    conn.commit()

    cursor.execute("UPDATE course{} SET Column_{}_k = '{}' WHERE id={}".format(course, groupe, cab, id))
    conn.commit()


# -------------------------ДЛЯ ТЕСТИНГА ФУНКЦИЙ РАСКОМЕНТИТЬ:
# print(schedule_now(datetime.now(), 101))
# print(schedule_today(datetime.now(), 202))
# print(schedule_tomorrow(datetime.now(), 101))
# print(number_para(datetime.now()))
# print(change_classroom(202, 'Номер кабинета'))
