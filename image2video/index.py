import subprocess
import os

def images_to_video_with_audio(image_folder, audio_file, output_video, fps=30):
    """
    将文件夹中的图片合成为一个视频，并添加音频。

    :param image_folder: 包含图片的文件夹路径
    :param audio_file: 音频文件路径
    :param output_video: 输出视频的文件路径
    :param fps: 视频的帧率
    """
    # 确保图片文件夹和音频文件存在
    if not os.path.exists(image_folder):
        raise FileNotFoundError(f"图片文件夹 {image_folder} 不存在")
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"音频文件 {audio_file} 不存在")

    # 构建 FFmpeg 命令
    cmd = [
        'ffmpeg',
        '-y',  # 覆盖输出文件
        '-framerate', str(fps),  # 设置帧率
        '-i', os.path.join(image_folder, '%d.jpg'),  # 输入图片格式
        '-i', audio_file,  # 输入音频文件
        '-c:v', 'libx264',  # 视频编码
        '-pix_fmt', 'yuv420p',  # 像素格式
        '-c:a', 'aac',  # 音频编码
        '-map', '0:v',  # 映射视频流
        '-map', '1:a',  # 映射音频流
        '-shortest',  # 使视频和音频长度一致
        output_video  # 输出视频路径
    ]

    # 执行 FFmpeg 命令
    subprocess.run(cmd, check=True)

if __name__ == '__main__':

    # 示例使用
    image_folder = 'path/to/your/images'
    audio_file = 'path/to/your/audio.mp3'
    output_video = 'output_with_audio.mp4'
    fps = 30

    images_to_video_with_audio(image_folder, audio_file, output_video, fps)