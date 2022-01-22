import sys
from os.path import dirname, join, abspath
from telebot import types
from datetime import datetime

import EmojiAlphabet

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from SoftUbot import TIME as time
from SoftUbot.settings import conn, cursor


def schedule_main():
    keyboard_schedule = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text='Сейчас', callback_data='now')
    key_2 = types.InlineKeyboardButton(text='Сегодня', callback_data='today')
    key_3 = types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow')
    key_4 = types.InlineKeyboardButton(text='Неделя', callback_data='weak')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')
    keyboard_schedule.add(key_1)
    keyboard_schedule.add(key_2, key_3)
    keyboard_schedule.add(key_4)
    keyboard_schedule.add(key_back)

    msg = 'Окей, выбери какое расписание тебя интересует:'

    return keyboard_schedule, msg


def now(groupe, leader):
    t = datetime.now()  # узнает время сейчас
    seychas = time.schedule_now(t, groupe)

    if leader and seychas[1]:

        msg = 'Сейчас у тебя - <b> {}! </b> \n\nВедёт пару -  <b>{}.</b> \n\n А проходит это в<b> {} </b>кабинете'.format(
            seychas[0]['name'], seychas[0]['teacher'], seychas[0]['cab'])

        keyboard_schedule_leader = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Изменить кабинет', callback_data='change_cab')
        key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_schedule')
        keyboard_schedule_leader.add(key_1)
        keyboard_schedule_leader.add(key_back)

        return keyboard_schedule_leader, msg

    else:

        msg = 'Сейчас у тебя - <b> {}! </b> \n\nВедёт пару -  <b>{}.</b> \n\n А проходит это в<b> {} </b>кабинете'.format(
            seychas[0]['name'], seychas[0]['teacher'], seychas[0]['cab'])

        keyboard_schedule_back = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_schedule')
        keyboard_schedule_back.add(key_back)

        return keyboard_schedule_back, msg


def change_classroom(groupe, cab):
    keyboard_schedule_leader = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Изменить кабинет', callback_data='change_cab')
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_schedule')

    keyboard_schedule_leader.add(key_1)
    keyboard_schedule_leader.add(key_back)

    try:
        time.change_classroom(groupe, cab)  # сама функция по изменению тут в ФАЙЛЕ TIME

        msg = 'Ты успешно добавил(а) ссылку на конференцию!'

        return keyboard_schedule_leader, msg

    except Exception:
        msg = 'Не удалось поставить твою ссылку! Попробуй ещё раз позже!'

        return keyboard_schedule_leader, msg


def today(groupe):

    day = time.schedule_today(datetime.now(), groupe)

    msg = '<code>Вот список пар на СЕГОДНЯ:</code> \n\n\U0001F551<b>1-я пара (9:00 - 10:30):' \
          '</b>\n {} \nКабинет: {} \n\n\U0001F551<b>2-я пара (10:40 - 12:10):' \
          '</b>\n {} \nКабинет: {}  \n\n\U0001F551<b>3-я пара (12:50 - 14:20):' \
          '</b>\n {} \nКабинет: {} \n\n\U0001F551<b>4-я пара (14:30 - 16:00):' \
          '</b>\n {} \nКабинет: {} \n\n\U0001F551<b>5-я пара (16:10 - 17:40):' \
          '</b>\n {} \nКабинет: {}' \
        .format(
        day['para_1']['name'], day['para_1']['cab'], day['para_2']['name'],
        day['para_2']['cab'], day['para_3']['name'], day['para_3']['cab'],
        day['para_4']['name'], day['para_4']['cab'], day['para_5']['name'],
        day['para_5']['cab'])

    keyboard_schedule_back = types.InlineKeyboardMarkup()
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_schedule')
    keyboard_schedule_back.add(key_back)

    return keyboard_schedule_back, msg


def tomorrow(groupe):
    day = time.schedule_tomorrow(datetime.now(), groupe)

    msg = '<code>Вот список пар на СЕГОДНЯ:</code> \n\n\U0001F551<b>1-я пара (9:00 - 10:30):' \
          '</b>\n {} \nКабинет: {} \n\n\U0001F551<b>2-я пара (10:40 - 12:10):' \
          '</b>\n {} \nКабинет: {}  \n\n\U0001F551<b>3-я пара (12:50 - 14:20):' \
          '</b>\n {} \nКабинет: {} \n\n\U0001F551<b>4-я пара (14:30 - 16:00):' \
          '</b>\n {} \nКабинет: {} \n\n\U0001F551<b>5-я пара (16:10 - 17:40):' \
          '</b>\n {} \nКабинет: {}' \
        .format(
        day['para_1']['name'], day['para_1']['cab'], day['para_2']['name'],
        day['para_2']['cab'], day['para_3']['name'], day['para_3']['cab'],
        day['para_4']['name'], day['para_4']['cab'], day['para_5']['name'],
        day['para_5']['cab'])

    keyboard_schedule_back = types.InlineKeyboardMarkup()
    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_schedule')
    keyboard_schedule_back.add(key_back)

    return keyboard_schedule_back, msg

def weak(groupe):
    course = str(groupe)[0]

    msg = 'Вот расписание на неделю в формате excel:'

    src = '/root/environments/bot/for_weak_schedule/course{}.xlsx'.format(course)

    doc = open(src, 'rb')

    keyboard_schedule_back_weak = types.InlineKeyboardMarkup()
    key_back = types.InlineKeyboardButton(text= EmojiAlphabet.back, callback_data='back_schedule_weak')
    keyboard_schedule_back_weak.add(key_back)

    return keyboard_schedule_back_weak, msg, doc

