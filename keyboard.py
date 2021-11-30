import telebot
from telebot import types

main_info = "Основная инфа"
event_timetable = "Программа мероприятия"
zones = "Зоны"
game = "Игра"
start_game = "Начать знакомство"
parts_number = "Количество участников"
finish_game = "Завершить игру"


def getStartKeyboard():
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.row(main_info, event_timetable)
    keyboard.row(zones, game)
    return keyboard


def getGameKeyboard():
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.row(start_game, parts_number)
    return keyboard


def getFinishGameKeyboard():
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.row(finish_game)
    return keyboard
