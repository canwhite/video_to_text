from TTS.api import TTS

# 初始化 TTS 模型
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

# 将文本转换为语音
text = "Hello, this is a test of Coqui TTS."
output_file = "output.wav"
tts.tts_to_file(text=text, file_path=output_file)

print(f"音频文件已保存到 {output_file}")
