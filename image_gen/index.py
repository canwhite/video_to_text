from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope
from pool import ThreadPool
import time

model = "flux-schnell"
client = dashscope.ImageSynthesis;


def simple_call(input_prompt,index):
    rsp = client.call(model=model,
                                        prompt=input_prompt,
                                        size='1024*1024')
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
        # save file to current directory
        for result in rsp.output.results:
            file_name = f"image_{index}.png"
            with open('./assets/images/%s' % file_name, 'wb+') as f:
                f.write(requests.get(result.url).content)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

'''
#need to:   
import threading 

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


# 命令模式，给到命令，封装执行
def batch_call(prompts, num_threads=5):
    thread_pool = ThreadPool(num_threads)
    results = []
    for index, prompt in enumerate(prompts):
        print(f"Processing prompt: {prompt}")
        res = thread_pool.apply(simple_call, (prompt, index))
        results.append(res)
        # need to import time
        # time.sleep(1)

    thread_pool.close()  # 阻止向线程池中添加新的任务
    thread_pool.join()   # 等待所有任务完成

    for res in results:
        file_name = res.get()
        if file_name:
            print(f"Generated image: {file_name}")
    # for res in results:
    #     res.get()



if __name__ == '__main__':
    # simple_call(prompt)
    prompts = ["Eagle flying freely in the blue sky and white clouds", "一只飞翔在蓝天白云的鹰"]
    batch_call(prompts)