import asyncio
import redis.asyncio as redis

# redis_client 是一个常量，它在整个程序中只有一个实例。常量通常在程序启动时初始化，并且在整个程序运行期间保持不变。
# 单例模式是一种设计模式，确保一个类只有一个实例，并提供一个全局访问点。单例模式通常通过类的静态方法或属性来实现。
# 在这个例子中，redis_client 是一个常量，而不是单例模式。它通过直接赋值的方式初始化，并且在整个程序中保持不变。
# 如果需要实现单例模式，可以使用类和静态方法来确保只有一个实例。
class RedisSingleton:
    _instance = None

    """
    __new__ 和 __init__ 是 Python 中用于创建和初始化对象的两个特殊方法。
    __new__ 方法是一个静态方法，用于创建对象的实例。它在对象实例化之前被调用，并返回一个新的实例。
    __init__ 方法是一个实例方法，用于初始化对象的属性。它在对象实例化之后被调用，并且不返回任何值。
    通常情况下，__new__ 方法用于控制对象的创建过程，而 __init__ 方法用于初始化对象的状态。
    在单例模式中，__new__ 方法通常用于确保只有一个实例被创建。
    """
    async def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = await redis.Redis(host='localhost', port=6379, db=0)
        return cls._instance

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