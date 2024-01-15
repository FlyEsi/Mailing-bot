from aiogram.types import ReplyKeyboardMarkup , KeyboardButton,ReplyKeyboardRemove
import config
from database import Database

db = Database()

main_menu = ReplyKeyboardMarkup(resize_keyboard = True)
main_menu.add("📩 Рассылка")
main_menu.add("Добавить пользователей")

next_ = ReplyKeyboardMarkup(resize_keyboard=True)
next_.add("➡️ Пропустить")


confim_maling = ReplyKeyboardMarkup(resize_keyboard = True)
confim_maling.add("Подтвердить рассылку")
confim_maling.add("◀️ Назад")

choose_action = ReplyKeyboardMarkup(resize_keyboard =True)
choose_action.add("✅ Отправить пост ","🔘 Добавить кнопки")
choose_action.add("◀️ Назад")

back = ReplyKeyboardMarkup(resize_keyboard=True)
back.add("◀️ Назад")


to_admin = ReplyKeyboardMarkup(resize_keyboard=True)
to_admin.add("◀️ В админку")



