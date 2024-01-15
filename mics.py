import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import asyncio


bot = Bot(config.TG_TOKEN,parse_mode="HTML")
storage = MemoryStorage()

dp = Dispatcher(bot, loop = asyncio.get_event_loop(),storage = storage)
logging.basicConfig(level=logging.INFO)

