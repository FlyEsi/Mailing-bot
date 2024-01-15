from os import environ
import configparser  # импортируем библиотеку

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

TG_TOKEN = config["settings"]["TG_TOKEN"]

#postgres конфигурация
POSTGRES_PASSWORD = config["settings"]["POSTGRES_PASSWORD"]
POSTGRES_USER = config["settings"]["POSTGRES_USER"]
POSTGRES_DATABSE = config["settings"]["POSTGRES_DATABSE"]
POSTGRES_IP = config["settings"]["POSTGRES_IP"]


ADMINS = [5056328919,188228452]
SUPPORT = -1002044140539


