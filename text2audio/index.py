from lib import singleton
from TTS.api import TTS


@singleton
class TTSTool():
    def __init__(self):
        # tts_models/en/ljspeech/tacotron2-DDC
        # tts_models/zh-CN/baker/tacotron2-DDC-GST
        # tts_models/zh-CN/baker/tacotron2-DDC-GST
        self.tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST", progress_bar=False, gpu=False)
    
    def tts_to_file(self, text, file_path):
        #max_decoder_steps=1000
        self.tts.tts_to_file(text=text, file_path=file_path) 


if __name__ == "__main__":
    # 将文本转换为语音
    text = "你好，我是张三。"
    output_file = "output.wav"

    tts = TTSTool()
    tts.tts_to_file(text=text, file_path=output_file)
