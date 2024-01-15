from mics import dp,bot
from database import Database
import text
from states import Mailing,FileLoaderState

from aiogram import types
import config
import asyncio
import keyboard

db = Database()

from aiogram_media_group import MediaGroupFilter, media_group_handler



@dp.message_handler(text="◀️ В админку",state="*",)
@dp.message_handler(commands = ["start"],state="*",chat_id=config.ADMINS)
async def message(message,state):
    await state.finish()
    await message.answer(text=text.admin,reply_markup=keyboard.default.main_menu)

@dp.message_handler(text = "📩 Рассылка",chat_id=config.ADMINS)
async def message(message):
    await message.answer(text = "ℹ️Отправьте сообщение , фото или видео",reply_markup = keyboard.default.back)
    await Mailing.text.set()

@dp.message_handler(text="Добавить пользователей",chat_id=config.ADMINS)
async def message(message):
    await message.answer(text = "Отправьте txt файл с пользователями.",reply_markup=keyboard.default.to_admin)
    await FileLoaderState.state.set()

@dp.message_handler(state = FileLoaderState,content_types=types.ContentType.DOCUMENT)
async def message(message):
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    await message.bot.download_file(file_path, "file.txt")
    with open("file.txt","r",encoding='utf-8') as file:
        users = file.read()
    count = 0
    for user_id in users.split("\n"):
        try:
            user_id=int(user_id.strip())
        except Exception as e:
            print(e)
            continue
        if await db.get_user(user_id):
            continue
        await db.add_user(user_id)
        count+=1
    await message.answer(text = f"Добавлено {count}",reply_markup=keyboard.default.main_menu)
@dp.message_handler(text = "◀️ Назад",state =Mailing.text)
async def back_to_main_menu(message,state):
    await message.answer(text = text.admin,
                         reply_markup = keyboard.default.main_menu)
    await state.finish()    

@dp.message_handler(text = "◀️ Назад",state =Mailing.action)
async def back_to_main_menu(message,state):
    await message.answer(text = text.admin,
                         reply_markup = keyboard.default.main_menu)
    await state.finish()    
    
    
@dp.message_handler(state = Mailing.text)
async def back_to_main_menu(message,state):
    #await message.answer("Рассылка началась",reply_markup = keyboard.default.main_menu)

    users = await db.get_all_users()
    await message.answer("Выберите действие",reply_markup = keyboard.default.choose_action)
    await state.update_data(message = message)
    await Mailing.action.set()
    
async def mailing(message,users,buttons,media):    
    num = 0
    dont_delivery = 0
    for user in users:
      try:    
        if media:
            await bot.send_media_group(user['id'],media)
        
        elif message.text:
            await bot.send_message(user['id'],message.html_text,reply_markup = buttons)
        elif message.photo:
            await bot.send_photo(user['id'],photo = message.photo[-1].file_id, caption = message.html_text,reply_markup = buttons)
        
        elif message.video:
            await bot.send_video(user['id'],video = message.video.file_id,caption = message.html_text,reply_markup = buttons)
        await asyncio.sleep(0.09)
        num += 1
        #await bot.send_message(chat_id=1272818,text ="yeywywyw")
      except Exception as e:
          print(e)
          dont_delivery += 1
          
    return num, dont_delivery


@dp.message_handler(MediaGroupFilter(), content_types=types.ContentType.PHOTO,state = Mailing.text)
@media_group_handler
async def album_handler(messages,state):
    media = types.MediaGroup()
    for message in messages:
        try:
            caption = message.html_text
        except:
            caption = None
        media.attach_photo(message.photo[-1].file_id,caption = caption)
    await message.answer("Выберите действие",reply_markup = keyboard.default.choose_action)
    await state.update_data(message = None,media = media)
    await Mailing.action.set()    

   
@dp.message_handler(content_types = types.ContentType.PHOTO,state = Mailing.text)
async def back_to_main_menu(message,state):
    #await message.answer("Рассылка началась",reply_markup = keyboard.default.main_menu)
    if not message.caption:
        return await message.answer(text = "Вы не добавили caption")
    users = await db.get_all_users()
    await message.answer("Выберите действие",reply_markup = keyboard.default.choose_action)
    await state.update_data(message = message)
    await Mailing.action.set()
    
    
@dp.message_handler(content_types = types.ContentType.VIDEO,state = Mailing.text)
async def back_to_main_menu(message,state):
    #await message.answer("Рассылка началась",reply_markup = keyboard.default.main_menu)
    if not message.caption:
        return await message.answer(text = "Вы не добавили caption")    
    users = await db.get_all_users()
    await message.answer("Выберите действие",reply_markup = keyboard.default.choose_action)
    await state.update_data(message = message)
    await Mailing.action.set()

@dp.message_handler(text = "✅ Отправить пост",state = Mailing.action)
async def back_to_main_menu(message,state):
    #await message.answer("Рассылка началась",reply_markup = keyboard.default.main_menu)
    users = await db.get_all_users()
    await message.answer("Рассылка началась\n",reply_markup = keyboard.default.main_menu)
					   
    message_ = (await state.get_data())['message']
    media = (await state.get_data()).get('media')
    await state.finish()
    num , dont_delivery = await mailing(message_,users,None,media)    
    text_ = f"""✅ Доставлено сообщений : {num}
🗑 Удаленных пользователь : {dont_delivery}"""
    await message.answer(text_)   

@dp.message_handler(text = "🔘 Добавить кнопки",state = Mailing.action)
async def message(message,state):
    await message.answer(text = text.mailing_add_link,reply_markup = keyboard.default.back)
    await Mailing.add_links.set()
    
@dp.message_handler(text = "◀️ Назад",state =Mailing.add_links)
async def back_to_main_menu(message,state):
    await message.answer(text = text.admin,
                         reply_markup = keyboard.default.main_menu)
    await state.finish()        
    
@dp.message_handler(state =Mailing.add_links)
async def message(message,state):
    lines = await parse_markup(message.text)
    try:
       buttons = await keyboard.inline.create_button(lines)
    except Exception as e:    
       print(f"Create markup: {e}")
       await message.answer("Неправильный формат")
       return
    message_ = (await state.get_data())['message']    
    media = (await state.get_data()).get("media")
    print(media)
    if media:
       await message.answer_media_group(media)
    elif message_.text:
        await message.answer(message_.html_text,reply_markup = buttons)
    elif message_.photo:
        await message.answer_photo(message_.photo[-1].file_id,message_.html_text,reply_markup =buttons)
    elif message_.video:
        await message.answer_video(message_.video.file_id,message_.html_text,reply_markup = buttons)
    
    await message.answer("Выберите действие",reply_markup =keyboard.default.confim_maling)
    await Mailing.confim.set()
    await state.update_data(buttons = buttons)
    
@dp.message_handler(text = "◀️ Назад",state =Mailing.confim)
async def back_to_main_menu(message,state):
    await message.answer(text = text.admin,
                         reply_markup = keyboard.default.main_menu)
    await state.finish()            


async def parse_markup(text):
    markup = []
    rows = text.split("\n")
    for row in rows:
        list = []
        columns = row.replace("[","").split("]")
        for column in columns:
            if column:
               list.append(column.split(" + "))
        markup.append(list)
    return markup    
    
    
@dp.message_handler(text = "Подтвердить рассылку",state = Mailing.confim)
async def back_to_main_menu(message,state):
    #await message.answer("Рассылка началась",reply_markup = keyboard.default.main_menu)
    users = await db.get_all_users()   
    await message.answer("Рассылка началась\n",reply_markup = keyboard.default.main_menu)
    message_ = (await state.get_data())['message']
    buttons = (await state.get_data())['buttons']  
    media = (await state.get_data()).get('media')
    await state.finish()
    num , dont_delivery = await mailing(message_,users,buttons,media)    
    text_ = f"""✅ Доставлено сообщений : {num}
🗑 Удаленных пользователь : {dont_delivery}"""
    await message.answer(text_)   
    
'''num , dont_delivery = await mailing(message,users)    
text_ = f"""✅ Доставлено сообщений : {num}
🗑 Удаленных пользователей : {dont_delivery}"""
    await message.answer(text_)   '''
