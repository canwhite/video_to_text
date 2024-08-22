from flask import Flask, request
import json
import libaudio 
import whisper
from pool import ThreadPool 
from deepseek import OpenAITool
from config import API_KEY
from word_segmentation import split_text_into_sentences
from text2audio import TTSTool
from image_gen import batch_call
from image2video import images_to_video_with_audio,cleanup_assets
import sys

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

def get_graph_post_from_video(video_path):

    base_text = get_base_text(video_path)
    text = get_optimize_text(base_text)
    save_new_audio_from_text(text)
    # 完成分词
    sentences = split_text_into_sentences(text)
    # TODO,抽取图片，组成文章


def get_text_from_video_or_audio(video_path):
    base_text = get_base_text(video_path)
    return base_text


def get_graph_video_from_video(video_path):

    # print(audioPath)
    base_text = get_base_text(video_path)

    text = get_optimize_text(base_text)

    save_new_audio_from_text(text)

    # 完成分词
    sentences = split_text_into_sentences(text)

    batch_call(sentences)

    # TOOD, 阿里百炼暂时不支持并发
    images_to_video_with_audio("./assets/images", "./assets/audios/output.wav", "./output.mp4")

    # 调用清理方法
    cleanup_assets("./assets/images", "./assets/audios")



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
    video_path = "/Users/zack/Desktop/test.mp4"
    get_graph_video_from_video(video_path)









