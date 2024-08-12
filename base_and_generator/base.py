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


def test_yield():

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

    # 使用生成器
    for item in main_generator():
        print(item)

    print('-----------------')

'''
TODO: 工厂方法，装饰器，发布订阅, 命令模式
'''
class Product:
    def __init__(self, name):
        self.name = name
    # __str__ 方法是 Python 中的一个特殊方法，用于定义对象的字符串表示形式。
    # 当你使用 print() 函数或调用 str() 函数来转换对象时，Python 会自动调用该对象的 __str__ 方法。
    def __str__(self):
        return f"Product: {self.name}"

class ProductFactory:
    @staticmethod
    def create_product(product_type):
        if product_type == "A":
            return Product("Type A")
        elif product_type == "B":
            return Product("Type B")
        else:
            raise ValueError("Unknown product type")


# product_a = ProductFactory.create_product("A")
# print(product_a)

# product_b = ProductFactory.create_product("B")
# print(product_b)


'''
一个发布订阅的例子
'''

class PubSub:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, fn):
        if not event_type in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(fn)

    def publish(self, event_type, data):
        if event_type in self.subscribers:
            for fn in self.subscribers[event_type]:
                fn(data)

# pubsub = PubSub()
# pubsub.subscribe('event_name', callback_function)
# pubsub.publish('event_name', data)


if __name__ == '__main__':

    test_yield()





    #PS，补充一点数组操作
    #--forEach
    # for index, item in enumerate(my_list):
    #     print(f"Index: {index}, Value: {item}")

    #--map 
    # [expression for item in iterable if condition]
    # 后边的if condition是可选的，满足条件才会到最终列表
    # sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    