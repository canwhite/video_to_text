# modal创建和操作
import peewee
import peewee_async
import asyncio


# TODO：因为原生使用太过于麻烦，所以使用peewee_async库

# TODO：peewee的初始化，创建一个数据库实例
database = peewee_async.PooledMySQLDatabase(
    'your_database_name',
    user='your_username',
    password='your_password',
    host='your_host',
    port=3306
)

# 定义一个基类，所有模型类都继承自这个基类
class BaseModel(peewee.Model):
    class Meta:
        database = database

# 定义一个具体的模型类
class User(BaseModel):
    username = peewee.CharField(unique=True)
    registration_date = peewee.DateTimeField()

# 创建表
database.set_allow_sync(False)  # 禁用同步操作
objects = peewee_async.Manager(database)

# 创建表（同步操作）
with objects.allow_sync():
    User.create_table(True)



# TODO: 一些使用操作后续再详细研究

async def create_user(username):
    user = await objects.create(User, username=username)
    return user

async def get_user(username):
    user = await objects.get(User, username=username)
    return user

async def main():
    # 创建用户
    user = await create_user('john_doe')
    print(f"Created user: {user.username}")

    # 获取用户
    user = await get_user('john_doe')
    print(f"Retrieved user: {user.username}")

# 运行异步主函数
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

#使用