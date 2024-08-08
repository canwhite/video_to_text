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

    #PS，补充一点数组操作
    #--forEach
    # for index, item in enumerate(my_list):
    #     print(f"Index: {index}, Value: {item}")

    #--map 
    # [expression for item in iterable if condition]
    # 后边的if condition是可选的，满足条件才会到最终列表
    # sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    