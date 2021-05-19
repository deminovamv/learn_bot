import ephem
from datetime import date


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
