import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import Column
from sqlalchemy import BigInteger, String

import os
from urllib.parse import quote_plus
# 数据库URL

encoded_password = quote_plus(os.getenv('SQL_PW'))

DATABASE_URL = "mysql+aiomysql://{username}:{password}@{ip}:{port}/{db_name}?charset=utf8".format(
            username="root",
            password=encoded_password,
            ip="127.0.0.1",
            port=3306,
            db_name="test"
        )
        
# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建基类
Base = declarative_base()


# 创建异步会话
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = 't_user'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(length=6), unique=True, comment='名字')


async def get_user():
    async with async_session() as session:
        async with session.begin():
            # 查询用户
            user = await session.get(User, 1)
            print(user.username)

# 获取所有users
async def get_all_users():
    async with async_session() as session:
        async with session.begin():
            # 查询所有用户
            result = await session.execute(select(User))
            users = result.scalars().all()
            for user in users:
                print(user.id, user.username)



async def create_user(username):
    async with async_session() as session:
        async with session.begin():
            # 创建新用户
            new_user = User(username=username)
            session.add(new_user)
            await session.commit()



async def init_db():

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # 删除所有表
        await conn.run_sync(Base.metadata.create_all)  # 创建所有表


    # await create_user("李四")
    await get_user()
    # await get_all_users()

    await engine.dispose()





if __name__ == '__main__':
    asyncio.run(init_db())
