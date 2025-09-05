


from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
)

from config import VIDEO_FPS, SCENE_DURATION
import os


def compose_video(story_text, project_dir, image_path, audio_path):
    """合成视频：单张图片配整个故事的音频"""
    from moviepy import ImageClip, AudioFileClip

    # 加载图片和音频
    img_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path)

    # 设置图片显示时长与音频等长
    img_clip = img_clip.with_duration(audio_clip.duration)

    # 将音频设置给图片剪辑
    video_clip = img_clip.with_audio(audio_clip)

    # 输出文件路径
    output_path = os.path.join(project_dir, "final_video.mp4")

    # 写入视频文件
    video_clip.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
    )

    # 关闭剪辑，释放资源
    video_clip.close()
    audio_clip.close()

    return output_path