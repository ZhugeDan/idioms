#  适用于 MoviePy 2.x（2.2.1 亲测）
from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
)
from config import VIDEO_FPS, SCENE_DURATION
import os


def compose_video(script, project_dir):
    """合成完整视频"""
    clips = []

    for i, scene in enumerate(script["scenes"]):
        # 1. 图像片段
        img_path = os.path.join(project_dir, f"scene_{i + 1}.png")
        img_clip = ImageClip(img_path).with_duration(SCENE_DURATION)

        # 2. 音频片段
        audio_clips = []

        # 旁白
        if scene.get("narration"):
            nar_path = os.path.join(project_dir, f"scene_{i + 1}_nar.wav")
            audio_clips.append(AudioFileClip(nar_path))

        # 对话
        for j, _ in enumerate(scene["dialogue"]):
            dia_path = os.path.join(project_dir, f"scene_{i + 1}_dia_{j + 1}.wav")
            audio_clips.append(AudioFileClip(dia_path))

        # 3. 把音频绑到图像上
        if audio_clips:
            composed_audio = CompositeAudioClip(audio_clips)
            img_clip = img_clip.with_audio(composed_audio)

        clips.append(img_clip)

    # 4. 串接全部片段
    final_video = concatenate_videoclips(clips)

    # 5. 输出
    output_path = os.path.join(project_dir, "final_video.mp4")
    final_video.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec="libx264",
        audio_codec="aac",
    )

    return output_path