from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import config

#функция для деления списка на ранвые части принмает список и количество элементов в раздельных списках
split_list = lambda categories, size: [categories[i:i+size] for i in range(0, len(categories), size)]



cancel = InlineKeyboardMarkup()
cancel.add(
    InlineKeyboardButton(text = "🚫 Отмена",callback_data="cancel")
)

to_main= InlineKeyboardMarkup()
to_main.add(InlineKeyboardButton(text = "⬅️ Назад", callback_data="main_menu"))

async def create_button(rows):
    "создаем кнопки из списка для пользователя (рассылка)"
    menu = InlineKeyboardMarkup()
    for row in rows:
        line = []
        for column in row:
          print(column)
          line.append(InlineKeyboardButton(text = column[0],url=column[1]))
        menu.add(*line)
    return menu    




