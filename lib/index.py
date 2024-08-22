import whisper

model = whisper.load_model("medium")


def get_audio_from_video(video_path):
    audio = whisper.load_audio("/Users/zack/Desktop/test.mp4")
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.pad_or_trim(audio)
    result = model.transcribe(audio)
    return result

def get_manual_full_text(result):
    manual_full_text = ""
    for segment in result["segments"]:
        manual_full_text += segment["text"] + " "
    manual_full_text = manual_full_text.strip()
    return manual_full_text

def get_base_text(video_path):
    result = get_audio_from_video(video_path)
    manual_full_text = get_manual_full_text(result);
    return manual_full_text

def get_optimize_text(base_text):
    tool = OpenAITool(API_KEY)
    role_des = "您是一个文本助手，会讲我给你的文本以一种更加令人舒适的方式讲出来, 除了《》不用加之后，其他按照文章节奏加上标点符号"
    question_des = "以下是文本内容: " + manual_full_text +""
    text = tool.request(role_des, question_des)
    return text

def get_graph_post_from_video(vio):
    base_text = get_base_text(video_path)
    text = get_optimize_text(base_text)

def save_new_audio_from_text(text):
    tts = TTSTool()
    output_file = "./assets/audios/output.wav"
    tts.tts_to_file(text=text, file_path=output_file)