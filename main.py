import telebot
from time import sleep
import datetime
import os

import mem_sender
import keyboard
import date_helper

BOT_TOKEN = ''
BOT_INTERVAL = 3
BOT_TIMEOUT = 30

bot = telebot.TeleBot(BOT_TOKEN)
party_date = datetime.datetime.today().replace(2021, 11, 26, 0, 0, 0)
memSender = None
all_memes = []

main_info = ""
timetable = ""
zones = ""
maintainer = ""

STANDART_INCORRECT_TIME_BOT_ANSWER = "Прости, еще рано. Мероприятие начнется через "


def init():
    global main_info, timetable, maintainer, zones

    f = open('main_info.txt', 'r', encoding="utf-8")
    for line in f:
        main_info += line
    f.close()

    f = open('timetable.txt', 'r', encoding="utf-8")
    for line in f:
        timetable += line
    f.close()

    f = open('zones.txt', 'r', encoding="utf-8")
    for line in f:
        zones += line
    f.close()

    f = open('maintainer.txt', 'r')
    maintainer = f.read()
    f.close()

    memsDir = 'mems'
    for dir, subdir, files in os.walk(memsDir):
        for file in files:
            all_memes.append(os.path.join(dir, file))


def bot_polling():
    global bot
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            init()
            bot_actions()
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex:
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else:
            bot.stop_polling()
            print("Bot polling loop finished")
            break


def define_zone_request_answer(message):
    is_correct_date = datetime.datetime.now() >= party_date
    if is_correct_date:
        bot.send_message(message.chat.id, zones, reply_markup=keyboard.getStartKeyboard())
    else:
        time_interval = date_helper.get_time_interval(party_date)
        bot.send_message(message.chat.id, STANDART_INCORRECT_TIME_BOT_ANSWER + time_interval,
                         reply_markup=keyboard.getStartKeyboard())


def define_game_request_answer(message):
    global memSender
    is_correct_date = datetime.datetime.now() >= party_date
    if is_correct_date:
        if memSender is None:
            memSender = mem_sender.MemSender()
        if message.chat.username == maintainer:
            bot.send_message(message.chat.id, "Отлично, начинаем. Id игры = " + str(memSender.game_id),
                             reply_markup=keyboard.getStartKeyboard())
            bot.send_message(message.chat.id, "Введите размер группы: ",
                             reply_markup=keyboard.getStartKeyboard())
        else:
            bot.send_message(message.chat.id, "Введи id игры:",
                             reply_markup=keyboard.getStartKeyboard())
    else:
        time_interval = date_helper.get_time_interval(party_date)
        bot.send_message(message.chat.id, STANDART_INCORRECT_TIME_BOT_ANSWER + time_interval,
                         reply_markup=keyboard.getStartKeyboard())


def define_id_request_answer(message):
    if int(message.text) == memSender.game_id:
        if message.chat.id not in memSender.participants:
            memSender.add_participant(message.chat.id)
        bot.send_message(message.chat.id, "Поздравляю ты в игре! Жди от меня мема 😎", reply_markup=keyboard.getStartKeyboard())
    else:
        bot.send_message(message.chat.id, "Неверный id!", reply_markup=keyboard.getStartKeyboard())


def define_group_number_answer(message):
    gr_number = int(message.text)
    if gr_number in range(2, 11):
        memSender.group_number = gr_number
        bot.send_message(message.chat.id, 'Отлично. Размер группы ' + message.text,
                         reply_markup=keyboard.getGameKeyboard())
    else:
        bot.send_message(message.chat.id, 'Не подойдет. Размер группы должен быть от 2 до 10 человек',
                         reply_markup=keyboard.getStartKeyboard())


def bot_actions():
    @bot.message_handler(commands=['start'], content_types=['text'])
    def send_welcome(message):
        if message.chat.type == 'private':
            bot.send_message(message.chat.id, "Привет, " + message.chat.first_name + "!",
                             reply_markup=keyboard.getStartKeyboard())

    @bot.message_handler(content_types=['text'])
    def bot_managering(message):
        global memSender
        if message.chat.type == 'private':
            if message.text == keyboard.main_info:
                bot.send_message(message.chat.id, main_info, reply_markup=keyboard.getStartKeyboard())
            elif message.text == keyboard.event_timetable:
                bot.send_message(message.chat.id, timetable, reply_markup=keyboard.getStartKeyboard())
            elif message.text == keyboard.zones:
                define_zone_request_answer(message)
            elif message.text == keyboard.game:
                define_game_request_answer(message)
            elif message.chat.username != maintainer and message.text.isdigit():
                define_id_request_answer(message)
            elif message.chat.username == maintainer and message.text.isdigit():
                define_group_number_answer(message)
            elif message.text == keyboard.parts_number:
                answer = "Количество участников: " + str(len(memSender.participants))
                bot.send_message(message.chat.id, answer, reply_markup=keyboard.getGameKeyboard())
            elif message.text == keyboard.start_game:
                memSender.send_memes(all_memes, bot)
                bot.send_message(message.chat.id, "Игра началась!", reply_markup=keyboard.getFinishGameKeyboard())
            elif message.text == keyboard.finish_game:
                memSender = None
                bot.send_message(message.chat.id, "Игра окончена", reply_markup=keyboard.getStartKeyboard())

