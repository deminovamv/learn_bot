import logging
from os import replace
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from datetime import date, datetime
import re 
import city_game



logging.basicConfig(filename="bot.log", level= logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}

# Уровень 2
# Реализуйте в боте команду /wordcount которая считает слова в присланной фразе. 
# Например на запрос /wordcount Привет как дела бот должен ответить: 3 слова. 
# Не забудьте:

# Добавить проверки на пустую строку
# Как можно обмануть бота, какие еще проверки нужны?


def wordcount(update, context):
    if update.message.text == '/wordcount':
        update.message.reply_text('Вы ввели только команду. '
        'Для того чтобы посчитать количество слов введите: '
        '/wordcount Привет как дела')
    else:
        text_sentence = re.sub(r'[^A-Za-zА-Яа-я\s]','', update.message.text)
        text_sentence = text_sentence.split()
        if len(text_sentence) == 1 :
            update.message.reply_text('Вы ввели только цифры или знаки припенания. '
        'Для того чтобы посчитать количество слов введите: '
        '/wordcount Привет как дела')
        else:
            update.message.reply_text(f'Количество слов: {len(text_sentence) - 1}')


# Уровень 2
# Реализуйте в боте команду, которая отвечает на вопрос “Когда ближайшее полнолуние?”
#  Например /next_full_moon 2019-01-01. Чтобы узнать, когда ближайшее полнолуние, используйте ephem.next_full_moon(ДАТА)


def next_full_moon(update, context):
    if update.message.text == '/next_full_moon':
        update.message.reply_text('Вы ввели только команду. '
        'Для того чтобы узнать дату близжайшего полнолуния введите: '
        '/next_full_moon 01.01.2019')
    else:
        text_date = update.message.text.split()
        st_date = text_date[1]
        for x in ('/','-','_','\\'):
            st_date = st_date.replace('/','.')
        try:
            dt = datetime.strptime(st_date, '%d.%m.%Y')
        except ValueError:
            update.message.reply_text(f'Введите дату в формате dd.mm.yyyy')
        dt = ephem.next_full_moon(dt)
        dt = datetime.strptime(str(dt), '%Y/%m/%d %H:%M:%S')
        update.message.reply_text('Ближайшее полнолуние будет: {}'.format(dt.strftime('%d.%m.%Y %H:%M:%S')))



Planet ={
  "Mars": "Марс",
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
    value = value.capitalize()
    for k, v in d.items():
        if v == value or k == value:
            return (k)

def name_planet(update, context):
    print(f'/planet')
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text('Пожалуйста, введите название планеты')
    else:
        # try:
             planet_name = text[1]
             if 'text' not in text:
                 key_planet = get_key(Planet,planet_name)
                 if key_planet:
                     planet_name = key_planet
             m = getattr(ephem, planet_name, 'error')
             if m == 'error':
                 update.message.reply_text('Это не похоже на название планеты, пожалуйста, попробуйте ещё раз')   
             else:
                 update.message.reply_text(f'Planet: {planet_name}')
                 m = m(date.today())
                 constellation = ephem.constellation(m)
                 update.message.reply_text(f'Date: {date.today()}')
                 update.message.reply_text(f'Constellation: {constellation[1]}')
        # except(AttributeError,TypeError):
            # update.message.reply_text('Это не похоже на название планеты, пожалуста, попробуйте ещё раз')



def greet_user(update, context):
    print(f'/start')
    name = update.message.chat.first_name
    update.message.reply_text(f'Привет, {name} 😊!')

    
def talk_to_me(update, context):
    text= update.message.text
    print(text)
    key_planet = get_key(Planet,text)
    if key_planet:
        update.message.text = 'text ' + key_planet
        name_planet(update, context)
    else:
        update.message.reply_text(text)

def main():
    mybot= Updater(settings.API_KEY, use_context= True, request_kwargs= PROXY)

    dp =  mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))    
    dp.add_handler(CommandHandler("planet", name_planet))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("cities", city_game.user_city_game))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('START')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()
    