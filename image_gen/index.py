from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope

# import replicate
# replicate 的api_token, 但是他们要钱太厉害了
# api_token = os.getenv('REPLICATE_API_TOKEN')
# api_token = 'r8_M3Ua2fS3WN9fPwv5Lo24i7ALdFx7BOS0kv6sd'

# # 初始化 Replicate 客户端
# client = replicate.Client(api_token=api_token)


# # 设置输入参数
# input_params = {
#     "prompt": "a photo of vibrant artistic graffiti on a wall saying \"SD3 medium\"",
#     "aspect_ratio": "3:2",
#     "image": "https://replicate.delivery/pbxt/LMbGi83qiV3QXR9fqDIzTl0P23ZWU560z1nVDtgl0paCcyYs/cars.jpg"
# }

# # 运行模型
# output = client.run(
#     "meta/sam-2:fe97b453a6455861e3bac769b441ca1f1086110da7466dbb65cf1eecfd60dc83",
#     input=input_params
# )


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