import aiohttp
import asyncio

# yield 在一个函数中用于生成迭代器
def sub_generator():
    yield 1
    yield 2
    yield 3


# yield from 用于在一个迭代器中调用另一个迭代器，简化迭代器成器的嵌套调用
def main_generator():
    yield 'A'
    # 注意yeild from 会自动调用子生成器，不需要 yield, 而且必须接受一个迭代器
    yield from sub_generator()
    yield 'B'


async def fetch(url):
    # async with 是用于异步上下文管理器的语法。
    # 异步上下文管理器必须实现 __aenter__ 和 __aexit__ 方法，
    # 这些方法返回异步可等待对象
    # async with aiohttp.ClientSession() as session: 确保会话在进入和退出上下文时被正确创建和关闭。
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def test_async():
    urls = [
        'https://www.python.org',
        'https://www.github.com'
    ]
    tasks = [fetch(url) for url in urls]
    responses = await asyncio.gather(*tasks)
    for url, response in zip(urls, responses):
        print(f"URL: {url}\nResponse: {response[:100]}...")


if __name__ == '__main__':

    gen = sub_generator()
    # 手动调用生成器
    print(next(gen))  # 输出: 1
    print(next(gen))  # 输出: 2
    print(next(gen))  # 输出: 3

    print('-----------------')

    main = main_generator()
    print(next(main))
    print(next(main))
    print(next(main))


    print('-----------------')

    # 使用生成器
    for item in main_generator():
        print(item)

    
    print('-----------------')

    # 运行异步主函数
    asyncio.run(test_async()) 
