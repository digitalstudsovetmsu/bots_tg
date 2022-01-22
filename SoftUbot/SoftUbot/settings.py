import psycopg2
import os, sys

PROJECT_ROOT = os.path.dirname(__file__)
print(PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'users'))

# подключаем БД
conn = psycopg2.connect(dbname='mytestdb', user='mytestuser',
                        password='51705170', host='89.108.64.97')
cursor = conn.cursor()  # обращаться будем через курсор

BotToken = '928197350:AAH5MzOU1Iwtb02v1xjYDloygFKFgefIePU'  # это API бота @mse_soft_u_bot

# -------------------------ВСЕ ОСНОВНЫЕ ТЕКСТОВЫЕ ФАЙЛЫ ------------------------------------------------------------

text_starter = "Привет! Меня зовут <b> MSE-MSU BOT</b> " + '\n \n' + 'Через меня можно узнавать <i>РАСПИСАНИЕ на учебную неделю</i>, ' \
                                                                     '\n можно ' \
                                                                     '<i>отметиться на ' \
                                                                     'паре</i>, если ты, ' \
                                                                     'конечно, ' \
                                                                     'на ней находишься, ' \
                                                                     'и даже узнать ' \
                                                                     '<i>ДЗ</i>.\n \n' \
                                                                     'Подробнее можно ' \
                                                                     'ознакомиться с ' \
                                                                     'проектом, ' \
                                                                     'нажав кнопку <b>"О ' \
                                                                     'нас"</b>. '

text_info = '\U00002139<b> Немного о нас!</b>' \
            '\n\nПроект по созданию ботов мы запустили довольно давно. На сегодняшний день во многих институтах плохо ' \
            'развита система отображения расписаний.' \
            ' Для того чтобы посмотреть текущее расписание, нужно зайти на сайт, а потом скачать неудобную таблицу.' \
            '\n\nВ связи с этим, нами было принято решение собрать команду разработчиков, которые смогли бы ' \
            'трансформировать расписание вузов в пару кнопок. ' \
            'Наши боты уже зарекомендовали себя на рынке. Они славятся своей простотой использования.' \
            '\n\nВы можете купить наше ПО на сайте -  softwareu.ru !'

text_help = '<b>Контакты поддержки:</b>\n\n\U0000260E' \
            'Телефон: +7(964)723-56-82\n\U0001F4E7' \
            'Email: #наша_корпоративная_почта\n\U0001F468\U0000200D\U0001F4BB' \
            'Технический директор - @grom_1337'

groupe_list = ['101', '102', '103', '104', '201', '202', '203', '204', '301', '302', '303', '304', '401', '402',
               '403', '404', '501', '502']

groupe_list_2 = ['100', '101', '102', '103', '104', '200', '201', '202', '203', '204', '300', '301',
                 '302', '303', '304', '400', '401',
                 '402',
                 '403', '404', '500', '501', '502']


def subject_list():
    cursor.execute("SELECT ОГД FROM table_info")
    subjects_1 = [item[0] for item in cursor.fetchall()]
    conn.commit()

    cursor.execute("SELECT ЭММЭ FROM table_info")
    subjects_2 = [item[0] for item in cursor.fetchall()]
    conn.commit()

    cursor.execute("SELECT ЭиФС FROM table_info")
    subjects_3 = [item[0] for item in cursor.fetchall()]
    conn.commit()

    cursor.execute("SELECT ОЭТ FROM table_info")
    subjects_4 = [item[0] for item in cursor.fetchall()]
    conn.commit()

    subjects = subjects_1 + subjects_2 + subjects_3 + subjects_4

    result = list(filter(None, subjects))

    # subjects_1.clear()
    # subjects_2.clear()
    # subjects_3.clear()
    # subjects_4.clear()
    # subjects.clear()
    # result.clear()

    return result  # убирает все None из списка


# print(subject_list())
# print(subject_list())
