# peewee_async 如何使用，现在users表结构是这样的
# +----+-------------------------+-------------------------+------------+----------+------+
# | id | created_at              | updated_at              | deleted_at | name     | age  |
# +----+-------------------------+-------------------------+------------+----------+------+
# |  2 | 2023-05-31 07:21:00.023 | 2023-06-03 03:32:06.324 | NULL       | zhagnsan |   88 |
# +----+-------------------------+-------------------------+------------+----------+------+

import peewee
import peewee_async
import datetime

# 创建一个数据库实例
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
    id = peewee.IntegerField(primary_key=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now)
    deleted_at = peewee.DateTimeField(null=True)
    name = peewee.CharField()
    age = peewee.IntegerField()

    class Meta:
        table_name = 'users'

# 禁用同步操作
# 禁用同步操作意味着在异步环境中，所有数据库操作都应该通过异步方法来执行，以避免阻塞事件循环。
# 这样可以确保应用程序在高并发情况下保持高性能和响应性。
# 在peewee_async中，通过调用`database.set_allow_sync(False)`来禁用同步操作，确保所有数据库操作都通过异步管理器`objects`来执行。

database.set_allow_sync(False)
# 创建异步管理器
objects = peewee_async.Manager(database)

# 允许同步操作的原因：
# 创建表这样的操作通常只需要在应用程序启动时执行一次，因此可以使用同步操作来完成。
# 通过调用 `with objects.allow_sync():`，我们可以在需要时临时允许同步操作，而不影响整体的异步环境。

# 如果表已经创建了，这里还会执行吗？
# 如果表已经存在，`User.create_table(True)` 不会再次创建表，而是会跳过创建操作。
# `True` 参数表示如果表已经存在，则不会引发错误。


with objects.allow_sync():
    User.create_table(True)
