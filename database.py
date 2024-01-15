import asyncpg

import config
from mics import dp
import asyncio

        
        
async def create_pool():
    return await asyncpg.create_pool(
                user= config.POSTGRES_USER,
                password =config.POSTGRES_PASSWORD,
                database = config.POSTGRES_DATABSE,
                host = config.POSTGRES_IP
                )
loop = asyncio.get_event_loop()
db = loop.run_until_complete(create_pool())

class Database:
    pool = db     
    
    async def create_table_users(self):
        sql = '''create table  if not exists users(
        id bigint,
        username text,
        balance decimal(10,2) default 0,
        refid bigint,
        purchase decimal(10,2) default 0)
        '''
        async with self.pool.acquire() as connect:
            select = await connect.execute(sql)
            
    
    async def add_user(self,id):
        sql = "insert into users(id) values($1)"
        async with self.pool.acquire() as connect:
            select = await connect.execute(sql,id) 
    
    
    async def get_user(self,id):
        sql = "select * from  users where id=$1"
        async with self.pool.acquire() as connect:
            select = await connect.fetchrow(sql,id)                     
        return select       
        
    
    async def update_username(self,id,username):
        sql = "update users set username = $1 where id = $2"
        async with self.pool.acquire() as connect:
            select = await connect.fetchrow(sql,username,id)                     
        return select   
        
    async def get_all_users(self):
        sql = "select * from  users"
        async with self.pool.acquire() as connect:
            select = await connect.fetch(sql)                     
        return select            
        
    
    
           
