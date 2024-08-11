from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope


model = "flux-schnell"
prompt = "Eagle flying freely in the blue sky and white clouds"
prompt_cn = "一只飞翔在蓝天白云的鹰" # Prompt支持中英文


def simple_call(input_prompt):
    rsp = dashscope.ImageSynthesis.call(model=model,
                                        prompt=input_prompt,
                                        size='1024*1024')
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
        # save file to current directory
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(result.url).content)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))


if __name__ == '__main__':
    # simple_call(prompt)
    simple_call(prompt_cn)