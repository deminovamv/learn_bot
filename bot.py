"""
Домашнее задание №1
Использование библиотек: ephem
* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.
"""


import logging
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from datetime import date


logging.basicConfig(filename="bot.log", level= logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}


Planet ={
  "Mars":"Марс",
  "Mercury":"Меркурий",
  "Venus":"Венера",
  "Jupiter":"Юпитер",
  "Saturn":"Сатурн",
  "Uranus":"Уран",
  "Neptune":"Нептун",
  "Pluto":"Плутон",
  "Sun":"Солнце",
  "Moon":"Луна"
}

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return (k)

def name_planet(update, context):
    print(f'/planet')
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text('Пожалуйста, введите название планеты в формате \'/planet Mars\'')
    else:
        try:
             planet_name = text[1].capitalize()
             key_planet = get_key(Planet,planet_name)
             if key_planet:
                 planet_name = key_planet
             m = getattr(ephem, planet_name)(date.today())
             update.message.reply_text(f'Planet: {planet_name}')
             constellation = ephem.constellation(m)
             update.message.reply_text(f'Date: {date.today()}')
             update.message.reply_text(f'Constellation: {constellation[1]}')
        except(AttributeError,TypeError):
            update.message.reply_text('Это не похоже на название планеты, пожалуста, попробуйте ещё раз')



def greet_user(update, context):
    print(f'/start')
    name = update.message.chat.first_name
    update.message.reply_text(f'Привет, {name} 😊! ')
    
def talk_to_me(update, context):
    text= update.message.text
    print(text)
    update.message.reply_text(text)

def main():
    mybot= Updater(settings.API_KEY, use_context= True, request_kwargs= PROXY)

    dp =  mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))    
    dp.add_handler(CommandHandler("planet", name_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('START')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()