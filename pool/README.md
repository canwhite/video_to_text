```
用python实现真正意义上的多线程’
在 Python 中实现真正的多线程可能会遇到一些困难，
这主要是因为 Python 的全局解释锁（GIL）限制了同一时间只能有一个线程在解释器中执行字节码。
因此，尽管 Python 有 threading 模块支持多线程，但这些线程并不是真正的并行执行，特别是在 CPU 密集型任务中。
但是，还有一些方法可以帮你实现并发执行。


1）multiprocessing模块：这个模块运行在多个进程中的程序可以并发执行，从而避开了 GIL 的限制。
每个进程有自己的内存空间和 Python 解释器。你可以使用此模块中的 Process 类创建进程，然后使它们并行执行。

from multiprocessing import Process
def f(name):
    print('hello', name)
if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()



PS：线程池呢
from multiprocessing import Pool
def f(x):
    return x*x
if __name__ == '__main__':
    with Pool(5) as p:
        res = p.apply_async(f, (4,))  # 使用 apply_async 方法提交单个任务
        print(res.get(timeout=1))  # 使用 get 方法获取结果，可以指定一个超时时间



2）concurrent.futures模块：这个模块提供了一个高级的接口，可以很容易实现异步操作。


from concurrent.futures import ThreadPoolExecutor
def worker(x):
    # 将此函数内的任务并发执行
    return x * x
with ThreadPoolExecutor() as executor:
    future = executor.submit(worker, 2)  # 返回一个 Future 对象
    print(future.result())

3）asyncio模块：如果你编写的是 I/O 密集型的应用（如网络服务），
那么使用 asyncio 模块配合「协程」可以实现异步 I/O，提高程序的并发性。

import asyncio
async def main():
    print('Hello')
    await asyncio.sleep(1)
    print('World')
asyncio.run(main())

如果你的任务主要是 CPU 密集型的，使用multiprocessing模块是更好的选择。如果你的任务主要是 I/O 密集型的，如网络请求或文件读写，那么使用asyncio模块通常可以得到更好的性能。
```
