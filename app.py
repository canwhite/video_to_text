from flask import Flask, request
import json
import libaudio 
import whisper
from pool import ThreadPool 
from request import OpenAITool
from config import API_KEY
from word_segmentation import split_text_into_sentences
from text2audio import TTSTool
from image_gen import batch_call
from image2video import images_to_video_with_audio,cleanup_assets

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


#  creative process
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

    model = whisper.load_model("small")
    audio = whisper.load_audio("/Users/zack/Desktop/test.mp4")
    audio = whisper.pad_or_trim(audio)
    result = model.transcribe(audio)
    # print(result["text"])
    # full_result = ''
    # for batch in result["batches"]:
    #     full_result += ' '.join([segment['text'] for segment in batch['segments']])
    # print(full_result)
    print(result)
    manual_full_text = ""
    for segment in result["segments"]:
        manual_full_text += segment["text"] + " "
    manual_full_text = manual_full_text.strip()
    print("手动拼接文本:", manual_full_text)

    # 将以下内容根据上下文纠正错误，并用更加令人舒适的方法表述一下
    tool = OpenAITool(API_KEY)
    role_des = "您是一个助手，会讲我给你的文本以一种更加令人舒适的方式讲出来, 注意根据节奏加上标点符号"
    question_des = "以下是文本内容: " + manual_full_text +""
    text = tool.request(role_des, question_des)

    # 将文本转为音频暂存本地
    tts = TTSTool()
    output_file = "./assets/audios/output.wav"
    tts.tts_to_file(text=text, file_path=output_file)


    # 完成分词
    sentences = split_text_into_sentences(text)
    print("Sentences:", sentences)

    # 将sentences生成图片   
    batch_call(sentences)

    # 合成视频
    images_to_video_with_audio("./assets/images", "./assets/audios/output.wav", "./output.mp4")

    # 调用清理方法
    cleanup_assets("./assets/images", "./assets/audios")


    


    







