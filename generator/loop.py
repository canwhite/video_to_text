import asyncio

# 模拟异步操作的协程
async def async_operation(duration):
    await asyncio.sleep(duration)  # 使用 asyncio.sleep 模拟异步操作
    return f"Operation completed after {duration} seconds"

# 使用生成器模拟异步操作
def async_generator():
    loop = asyncio.get_event_loop()
    result = yield loop.run_until_complete(async_operation(1))
    print(result)
    result = yield loop.run_until_complete(async_operation(2))
    print(result)
    result = yield loop.run_until_complete(async_operation(3))
    print(result)

# 驱动生成器的函数
def run_generator(gen):
    try:
        next(gen)  # 启动生成器
        while True:
            result = gen.send(None)  # 发送 None 以继续生成器
            next(gen)  # 继续生成器
    except StopIteration:
        pass

if __name__ == '__main__':

    gen = async_generator()
    run_generator(gen)