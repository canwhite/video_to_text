import asyncio
import aiohttp

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
    # 使用生成器
    asyncio.run(test_async())