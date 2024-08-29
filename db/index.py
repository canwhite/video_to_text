import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import Column
from sqlalchemy import BigInteger, String
from sqlalchemy import select, text
import os
from urllib.parse import quote_plus
# 数据库URL

encoded_password = quote_plus(os.getenv('SQL_PW'))


# 主义这里的mysql+aiomysql，制定了sql操作的驱动
DATABASE_URL = "mysql+aiomysql://{username}:{password}@{ip}:{port}/{db_name}?charset=utf8".format(
            username="root",
            password=encoded_password,
            ip="127.0.0.1",
            port=3306,
            db_name="test"
        )
        
# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建异步会话
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# 创建基类
Base = declarative_base()

# 根据基类创建模型
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


async def create_user(username):
    async with async_session() as session:
        async with session.begin():
            # 创建新用户
            new_user = User(username=username)
            session.add(new_user)
            await session.commit()


# 获取所有users
async def get_all_users():
    async with async_session() as session:
        async with session.begin():
            # 查询所有用户
            result = await session.execute(select(User))
            users = result.scalars().all()
            for user in users:
                print(user.id, user.username)


async def get_all_users_by_sql():
    async with async_session() as session:
        async with session.begin():
            # 查询所有用户
            result = await session.execute(text("select * from t_user"))
            users = result.fetchall()
            users_list = []
            for user in users:
                user_obj = User(id=user[0], username=user[1])
                print(user_obj.id, user_obj.username)
                users_list.append(user_obj)


async def update_user(user_id, new_username):
    async with async_session() as session:
        async with session.begin():
            # 获取用户
            user = await session.get(User, user_id)
            if user:
                # 更新用户名
                user.username = new_username
                await session.commit()
                print(f"User {user_id} updated with new username: {new_username}")
            else:
                print(f"User {user_id} not found")



async def delete_user(user_id):
    async with async_session() as session:
        async with session.begin():
            # 获取用户
            user = await session.get(User, user_id)
            if user:
                # 删除用户
                await session.delete(user)
                await session.commit()
                print(f"User {user_id} deleted")
            else:
                print(f"User {user_id} not found")



async def init_table():
    """
    begin 方法在 SQLAlchemy 中用于开始一个事务。在异步上下文中，使用 `async with session.begin()` 可以确保在进入 `async with` 块时自动开始一个事务，
    # 并在退出块时自动提交事务（如果事务成功）或回滚事务（如果发生异常）。
    
    具体来说：
    - 进入 `async with session.begin()` 块时，事务开始。
    - 在块内执行的所有数据库操作都在同一个事务中。
    - 如果块内的所有操作都成功，事务将自动提交。
    - 如果块内发生异常，事务将自动回滚，确保数据的一致性。
    """
    async with engine.begin() as conn:
        # 删除所有表的操作是为了确保数据库结构的初始化。如果不删除所有表，可能会导致表结构不一致或遗留旧表的问题。
        # 但是，删除所有表会清除所有数据，因此在生产环境中应谨慎使用。如果不需要删除所有表，可以跳过这一步。
        # 如果你确定不需要删除所有表，可以注释掉或删除以下这行代码：
        # await conn.run_sync(Base.metadata.drop_all)

        # 创建所有表,已经有的不会再创建
        await conn.run_sync(Base.metadata.create_all)

    


async def init_db():


    init_table()

    # await create_user("李四")
    await get_user()
    # await get_all_users()

    await get_all_users()

    await get_all_users_by_sql()

    # 这行代码 `await engine.dispose()` 用于关闭数据库引擎。
    # 在异步编程中，确保资源正确释放是非常重要的。关闭数据库引擎可以释放相关的资源，避免资源泄漏。
    await engine.dispose()



if __name__ == '__main__':
    asyncio.run(init_db())
