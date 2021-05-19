import logging
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import planet


logging.basicConfig(filename="bot.log", level= logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}



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
    dp.add_handler(CommandHandler("planet", planet.name_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('START')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()