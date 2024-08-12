from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope


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

# 命令模式，给到命令，封装执行
def batch_call(prompts):
    for index, prompt in enumerate(prompts):
        print(f"Processing prompt: {prompt}")
        simple_call(prompt,index)



if __name__ == '__main__':
    # simple_call(prompt)
    prompts = ["Eagle flying freely in the blue sky and white clouds", "一只飞翔在蓝天白云的鹰"]
    batch_call(prompts)