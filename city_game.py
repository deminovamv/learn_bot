# Уровень 3
# Научите бота играть в города. Правила такие - внутри бота есть список городов, пользователь пишет /cities Москва и если в списке такой город есть, бот отвечает городом на букву "а" - "Альметьевск, ваш ход". 
# Оба города должны удаляться из списка.

# Помните, с ботом могут играть несколько пользователей одновременно
import bot  

def get_city():
    cities = []
    with open("list_city.txt", 'r', encoding ='utf-8') as file_reader:
        cities = [line.rstrip() for line in file_reader]
    return cities


def binary_search(list, item, city = ''):
    low = 0
    high = len(list) - 1

    while low <= high:
        mid = int((low + high) / 2)
        guess = list[mid]
        if guess[0] == item and guess != city:
            return mid
        if guess[0] > item:
            high = mid -1
        else:
            low = mid + 1
    return None


def city_game(update, context, cities):
    city = update.message.text.split()
    city = city[1]
    if not city in cities:
        update.message.reply_text(f'такого города нет')
    else:
        letter = city[-1]
        letter = letter.upper()
        index = binary_search(cities, letter, city)
        if index:
             update.message.reply_text('{} , ваш ход'.format(cities.pop(index)))
             cities.remove(city)
        else:
            update.message.reply_text(f'я не знаю города на букву {letter}, ты выйграл')
        

def user_city_game(update, context):
    if update.message.chat.id in context.user_data:
        city_dict = context.user_data[update.message.chat.id]
        city_game(update, context,city_dict)
    else:
        context.user_data[update.message.chat.id] = get_city()
        city_dict = context.user_data[update.message.chat.id]
        city_game(update, context,city_dict)
