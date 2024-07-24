from openai import OpenAI
from config import BASE_URL
#参数是class
def singleton(cls):
    instances = {}
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

#装饰
@singleton
class OpenAITool:
    def __init__(self,api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key, base_url=BASE_URL)

    #用async/await定义异步函数，用asyncio.run()调用
    def request(self, role_des, question_des):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                #定义角色
                {"role": "system", "content": role_des},

                {"role": "user", "content": question_des},
            ],
            stream=False
        )
        return response.choices[0].message.content
    
