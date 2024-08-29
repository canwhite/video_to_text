import asyncio
import redis.asyncio as redis

# redis_client 是一个常量，它在整个程序中只有一个实例。常量通常在程序启动时初始化，并且在整个程序运行期间保持不变。
# 单例模式是一种设计模式，确保一个类只有一个实例，并提供一个全局访问点。单例模式通常通过类的静态方法或属性来实现。
# 在这个例子中，redis_client 是一个常量，而不是单例模式。它通过直接赋值的方式初始化，并且在整个程序中保持不变。
# 如果需要实现单例模式，可以使用类和静态方法来确保只有一个实例。
class RedisSingleton:
    _instance = None
    """
    `cls` 是 Python 中的一个约定俗成的名称，用于表示类方法（class method）中的类本身。在 Python 中，类方法的第一个参数通常被命名为 `cls`，
    以表示该方法是对类进行操作的。这与实例方法中的 `self` 类似，`self` 表示实例本身。
    在这个上下文中，`cls` 代表 `RedisSingleton` 类。
    `__new__` 方法是一个类方法，用于创建类的实例。在这个方法中，`cls` 用于访问类的属性（如 `_instance`）和调用类的其他方法。
    例如，`cls._instance` 用于检查和设置类的单例实例。如果 `_instance` 为 `None`，则创建一个新的 Redis 连接实例并将其赋值给 `_instance`，从而确保整个程序中只有一个 Redis 连接实例。
    """
    async def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = await redis.Redis(host='localhost', port=6379, db=0)
        return cls._instance

    # 类方法和静态方法的区别：
    # 1. 类方法（@classmethod）：
    #    - 类方法的第一个参数是类本身（通常命名为cls），而不是实例（self）。
    #    - 类方法可以通过类名直接调用，不需要实例化类。
    #    - 类方法可以访问和修改类级别的属性（如类变量）。
    # 2. 静态方法（@staticmethod）：
    #    - 静态方法没有默认的第一个参数（既不是self也不是cls）。
    #    - 静态方法可以通过类名直接调用，不需要实例化类。
    
    @classmethod
    async def get_instance(cls):
        if not cls._instance:
            cls._instance = await redis.Redis(host='localhost', port=6379, db=0)
        return cls._instance


async def main():

    redis_client = await RedisSingleton.get_instance()
    """
    `async with` 语句用于异步上下文管理器，它可以确保在进入和退出上下文时自动管理资源。
    """
    async with redis_client as client:
        await client.set('my-key', 'value')
        value = await client.get('my-key')
        print(value)

asyncio.run(main())