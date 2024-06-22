from multiprocessing import Pool
class ThreadPool:
    def __init__(self, num_threads):
        self.pool = Pool(processes=num_threads)
    def apply(self, func, args):
        return self.pool.apply_async(func, args)


#test        
if __name__ == '__main__':
    thread_pool = ThreadPool(5)
    res = thread_pool.apply(f, (4,))
    print(res.get(timeout=1))