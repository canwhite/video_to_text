import asyncio
import aiomysql
import logging
# from config import DB_CONFIG
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, host="127.0.0.1", user="root", password = os.getenv("SQL_PW"), db="test", port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.conn = None
        self.cursor = None
    
    """
    __aenter__ 和 __aexit__ 是 Python 中用于实现上下文管理器的特殊方法。
        __aenter__ 方法在进入上下文管理器时被调用，通常用于初始化资源，例如打开文件或连接数据库。
        __aexit__ 方法在退出上下文管理器时被调用，通常用于清理资源，例如关闭文件或断开数据库连接。
    这两个方法通常与 `async with` 语句一起使用，以确保资源在异步操作中正确地被管理和释放。
    """
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def connect(self):
        if not self.conn or self.conn.closed:
            logger.info("Connecting to the database...")
            self.conn = await aiomysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                port=self.port,
                loop=asyncio.get_event_loop()
            )
            self.cursor = await self.conn.cursor()
            logger.info("Connected to the database.")

    async def close(self):
        if self.cursor:
            await self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed.")

    async def execute(self, query):
        try:
            await self.cursor.execute(query)
            result = await self.cursor.fetchall()
            return result
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

# model
class User:
    def __init__(self, user_id, created_at, updated_at, deleted_at, name, age):
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.name = name
        self.age = age
    

    def __repr__(self):
        return (f"User(user_id={self.user_id}, created_at={self.created_at}, "
                f"updated_at={self.updated_at}, deleted_at={self.deleted_at}, "
                f"name={self.name}, age={self.age})")

# orm
async def test_example(db):
    result = await db.execute("SELECT * FROM users")
    logger.info(f"Query result: {result}")

    users = []
    for row in result:
        user = User(user_id=row[0], created_at=row[1], updated_at=row[2], deleted_at=row[3], name=row[4], age=row[5])
        users.append(user)
    
    logger.info(f"Users: {users}")


async def main():

    '''
        config =  {
            "host": "127.0.0.1",
            "user": "root",
            "password": os.getenv("SQL_PW")
            "db": "test",
            "port": 3306
        }
        # 用一个obj代替分别传参, ** 表示解包，
        # ** 操作符主要用于解包字典。它可以将字典中的键值对解包成关键字参数传递给函数。
        # 如果你有其他类型的数据结构，比如列表或元组，你可以使用 * 操作符来解包它们，
        # 但这通常用于位置参数而不是关键字参数。

        async with Database(**DB_CONFIG) as db:
            await test_example(db)
    '''


    async with Database() as db:
        await test_example(db)


if __name__ == "__main__":
    asyncio.run(main())