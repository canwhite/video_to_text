from flask import Flask, request
import json
import libaudio 
from config import API_KEY
from word_segmentation import split_text_into_sentences
from image_gen import batch_call
from image2video import images_to_video_with_audio,cleanup_assets
import sys
from lib import *


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




# 这里的 __name__ 取得是当前模块的值。当模块被直接运行时，__name__ 的值为 "__main__"，当模块被作为库导入时，__name__ 的值为模块名。
app = Flask(__name__)

@app.route('/upload_video', methods=['POST'])
def upload_video():
    # 获取上传的视频文件
    video_file = request.files.get('video')
    if not video_file:
        return 'No video file uploaded', 400
    
    # 保存视频文件到本地
    video_path = "./uploads/video.mp4"
    video_file.save(video_path)
    
    # 处理视频文件
    get_graph_video_from_video(video_path)
    return 'Video processed successfully', 200




#  creative process，这里是服务员
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


    # app.run(port=8000, debug=True)
    




