from multiprocessing import Pool
import threading 

"""
1)apply_async和apply的区别：
apply_async 是异步执行函数的方法，它会立即返回一个 AsyncResult 对象 ，
允许你非阻塞地提交任务并稍后获取结果。
apply 是同步执行函数的方法，它会阻塞直到函数完成并返回结果。


2)其他相关方法包括：
- `map(func, iterable)`: 将函数应用于可迭代对象中的每个元素，并返回结果列表。
- `map_async(func, iterable)`: 异步版本的 `map`，返回一个 AsyncResult 对象。
- `apply(func, args)`: 同步版本的 `apply_async`，阻塞直到函数完成并返回结果。
- `close()`: 阻止更多任务提交到线程池，一旦所有任务完成，线程池将关闭。
- `join()`: 等待线程池中的所有任务完成。

"""

class ThreadPool:
    def __init__(self, num_threads):
        self.pool = Pool(processes=num_threads)
    def apply(self, func, args):
        return self.pool.apply_async(func, args)
    # join 方法用于等待线程池中的所有任务完成。它会阻塞调用它的线程，直到线程池中的所有任务都执行完毕。
    def join(self):
        self.pool.join()
    #在提交完所有任务后，你应该调用 close 方法，关闭注入，然后调用 join 方法等待所有任务完成。
    def close(self):
        self.pool.close()


# 两种池子使用，一种普通使用，实际上都可以啦，但是官方有限流，这就很恶心

'''
def batch_call(prompts, num_threads=5):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for index, prompt in enumerate(prompts):
            print(f"Processing prompt: {prompt}")
            future = executor.submit(simple_call, prompt, index)
            futures.append(future)

        for future in futures:
            file_name = future.result()
            if file_name:
                print(f"Generated image: {file_name}")
'''


'''
# 命令模式，给到命令，封装执行
def batch_call(prompts, num_threads=5):
    thread_pool = ThreadPool(5)
    results = []
    for index, prompt in enumerate(prompts):
        print(f"Processing prompt: {prompt}")
        res = thread_pool.apply(simple_call, (prompt, index))
        results.append(res)
        time.sleep(2)

    thread_pool.close()  # 阻止向线程池中添加新的任务
    thread_pool.join()   # 等待所有任务完成

    for res in results:
        file_name = res.get()
        if file_name:
            print(f"Generated image: {file_name}")
'''



'''
def batch_call(prompts):
    threads = []
    for index, prompt in enumerate(prompts):
        print(f"Processing prompt: {prompt}")

        thread = threading.Thread(target=simple_call, args=(prompt, index))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
'''





def add(x,y):
    return x+y

#TODO 
def base_test():
    pass
def mutex_test():
    pass

# TODO： base using of thread  and mutex    
if __name__ == '__main__':

    #pool的使用
    thread_pool = ThreadPool(5)
    res = thread_pool.apply(add, (4,5))
    thread_pool.close() #关闭任务注入
    thread_pool.join() #会等待完成
    print(res.get(timeout=1))

    #基本线程的使用










