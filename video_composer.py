from moviepy.editor import *
from config import VIDEO_FPS, SCENE_DURATION
import os


def compose_video(script, project_dir):
    """合成完整视频"""
    clips = []

    for i, scene in enumerate(script["scenes"]):
        # 创建图像片段
        img_path = os.path.join(project_dir, f"scene_{i + 1}.png")
        img_clip = ImageClip(img_path).set_duration(SCENE_DURATION)

        # 创建音频片段
        audio_clips = []

        # 添加旁白
        if scene.get("narration"):
            audio_path = os.path.join(project_dir, f"scene_{i + 1}_nar.wav")
            audio_clips.append(AudioFileClip(audio_path))

        # 添加对话
        for j, dialog in enumerate(scene["dialogue"]):
            audio_path = os.path.join(project_dir, f"scene_{i + 1}_dia_{j + 1}.wav")
            audio_clips.append(AudioFileClip(audio_path))

        # 合并音频
        if audio_clips:
            composed_audio = CompositeAudioClip(audio_clips)
            img_clip = img_clip.set_audio(composed_audio)

        clips.append(img_clip)

    # 合成最终视频
    final_video = concatenate_videoclips(clips)
    output_path = os.path.join(project_dir, "final_video.mp4")
    final_video.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path