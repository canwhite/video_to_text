from flask import Flask, request
import json
import libaudio 
import whisper

'''
#起个服务
app = Flask(__name__)
# 默认是get
@app.route('/')
def hello_world():
    # data = json.loads(request.get_data())
    # prompt  = data.get('prompt')
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def upload_file():
    # 获取文件
    file = request.files.get('file')
    # 保存文件
    file.save('test.mp3')
    return 'success'
'''


if __name__ == '__main__':
    '''
        if you wanna test the api
        curl -X POST \
        http://127.0.0.1:8000/speak \
        -H 'Content-Type: application/json' \
        -d '{"prompt": "Hello"}'

    '''

    # 验证了一下，自己生成的get_audio也是可行的，但是whisper本身就有从mp4中提取文本的能力，2333
    # name =  libaudio.get_audio("/Users/zack/Desktop/test.mp4")
    # print(name)
    # audioPath = name
    # print(audioPath)

    model = whisper.load_model("base")
    audio = whisper.load_audio("/Users/zack/Desktop/test.mp4")
    audio = whisper.pad_or_trim(audio)
    result = model.transcribe(audio)
    print(result["text"])


