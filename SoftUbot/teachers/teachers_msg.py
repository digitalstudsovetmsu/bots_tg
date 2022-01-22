from telebot import types
import EmojiAlphabet


def main_menu(username):
    keyboard_menu_teacher = types.InlineKeyboardMarkup()

    key_1 = types.InlineKeyboardButton(text=EmojiAlphabet.information + ' О нас ' + EmojiAlphabet.information,
                                       callback_data='info')
    key_2 = types.InlineKeyboardButton(text=EmojiAlphabet.profile + ' Личный кабинет ' + EmojiAlphabet.profile,
                                       callback_data='kabinet')
    key_3 = types.InlineKeyboardButton(text=EmojiAlphabet.bets + ' Расписание' + EmojiAlphabet.bets,
                                       callback_data='schedule')
    key_4 = types.InlineKeyboardButton(text=u"\U00002705" + ' Посещаемость' + u"\U00002705", callback_data='checked_me')
    key_5 = types.InlineKeyboardButton(text=u"\U0001F4D5" + ' Домашнее задание ' + u"\U0001F4D7",
                                       callback_data='home_work')

    keyboard_menu_teacher.add(key_3, key_4)
    keyboard_menu_teacher.add(key_5)
    keyboard_menu_teacher.add(key_2)
    keyboard_menu_teacher.add(key_1)

    msg = f'Добрый день, {username}! '

    return keyboard_menu_teacher, msg


def back_to_main_menu():
    keyboard_menu_back = types.InlineKeyboardMarkup()

    key_back = types.InlineKeyboardButton(text=EmojiAlphabet.back, callback_data='back_main_menu')

    keyboard_menu_back.add(key_back)

    return keyboard_menu_back


