from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup



class FileLoaderState(StatesGroup):
    state=State()
class Mailing(StatesGroup):
    text = State()
    action = State()
    add_links = State()
    confim = State()    