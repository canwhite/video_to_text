import asyncio

# 最原始操作
async def async_operation(duration):
    await asyncio.sleep(duration)  # 使用 asyncio.sleep 模拟异步操作
    return f"Operation completed after {duration} seconds"

# 原始操作的队列push
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
            #gen是内部有yield的函数，send()方法可以恢复生成器执行，并将yield表达式的值作为send()方法的返回值
            result = gen.send(None)  
            next(gen)  # 继续生成器
    except StopIteration:
        pass

if __name__ == '__main__':

    gen = async_generator()
    run_generator(gen)