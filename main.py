import asyncio
from aiogram import executor

import utils 
import handlers
from mics import dp
from database import Database
import utils

db = Database()

async def on_startup(x):
    """создаются таблички в бд если их нет"""
    await db.create_table_users()
    
    
    
 
 
def main():
    executor.start_polling(dp,skip_updates = True,on_startup = on_startup)
         
if __name__ == '__main__':
    main()   
