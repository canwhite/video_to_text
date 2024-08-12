import subprocess
import os
import glob
import wave

def cleanup_assets(image_folder, audio_folder):
    """
    清理图片和音频文件夹下的内容
    """
    # 删除图片文件夹下的所有文件
    for image_file in glob.glob(os.path.join(image_folder, '*')):
        os.remove(image_file)
        print(f"Deleted image file: {image_file}")

    # 删除音频文件夹下的所有文件
    for audio_file in glob.glob(os.path.join(audio_folder, '*')):
        os.remove(audio_file)
        print(f"Deleted audio file: {audio_file}")

def get_audio_duration(audio_file):
    """
    获取音频文件的时长（秒）
    """
    with wave.open(audio_file, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    return duration

def images_to_video_with_audio(image_folder, audio_file, output_video, fps=30):
    # 确保图片文件夹和音频文件存在
    if not os.path.exists(image_folder):
        raise FileNotFoundError(f"图片文件夹 {image_folder} 不存在")
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"音频文件 {audio_file} 不存在")

    # 获取图片文件列表
    image_files = sorted(glob.glob(os.path.join(image_folder, '*.png')))
    if not image_files:
        raise FileNotFoundError(f"图片文件夹 {image_folder} 中没有找到图片文件")

    # 获取音频时长
    audio_duration = get_audio_duration(audio_file)

    # 计算每张图片的显示时间
    num_images = len(image_files)
    image_duration = audio_duration / num_images

    # 计算帧率，以便每张图片展示7.5秒
    required_fps = 1/image_duration
    
    # 构建 FFmpeg 命令
    cmd = [
        'ffmpeg',
        '-y',  # 覆盖输出文件
        '-framerate', str(required_fps),  # 设置帧率
        '-pattern_type', 'glob',  # 使用 glob 模式匹配图片文件
        '-i', os.path.join(image_folder, '*.png'),  # 输入图片格式
        '-i', audio_file,  # 输入音频文件
        '-c:v', 'libx264',  # 视频编码
        '-pix_fmt', 'yuv420p',  # 像素格式
        '-c:a', 'aac',  # 音频编码
        '-map', '0:v',  # 映射视频流
        '-map', '1:a',  # 映射音频流
        '-t', str(audio_duration),  # 设置视频时长为音频时长
        output_video  # 输出视频路径
    ]

    # 执行 FFmpeg 命令
    subprocess.run(cmd, check=True)
if __name__ == '__main__':
    # 示例使用
    image_folder = 'path/to/your/images'
    audio_file = 'path/to/your/audio.mp3'
    output_video = 'output_with_audio.mp4'
    fps = 1

    images_to_video_with_audio(image_folder, audio_file, output_video, fps)