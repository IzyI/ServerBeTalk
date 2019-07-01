import asyncio
import asyncpg

class BD_PSQL:
    def __init__(self):
        self.pool=False

    async def create_conn(self):
        for i in range(3):
            try:
                self.pool= await asyncpg.create_pool(user=self.config.db_user,
                                                 password=self.config.db_password,
                                                 database=self.config.db_name,
                                                 host=self.config.db_host,
                                                     )
                
            except Exception as e:
                print(f'Несмог подключится к бд: {str(e)}, {i}')
                await self.close_conn()
                self.pool=False
        await asyncio.sleep(5)
        print(self.pool)
        await self.pool.close()
        print("close")


    async def close_conn(self):
        try:
            await self.pool.close()
        except Exception as e:
            print(f'Пытался закрыть conn: {e}')



