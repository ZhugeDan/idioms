import time
from idiom_processor import load_idioms_from_csv, create_project_folder
from story_generator import generate_story_script, save_story_script
from image_generator import generate_scene_image
from audio_generator import synthesize_speech
from video_composer import compose_video
from publisher import publish_to_platforms
from config import VOICE_MAPPING
import json
import os


def process_idiom(idiom, animal_a="大橘猫", animal_b="小兔子"):
    """处理单个成语的全流程"""
    print(f"\n开始处理成语: {idiom}")
    start_time = time.time()

    # 1. 创建项目目录
    project_dir = create_project_folder(idiom)
    print(f"项目目录: {project_dir}")

    # 2. 生成故事脚本
    script = generate_story_script(idiom, animal_a, animal_b)
    script_path = os.path.join(project_dir, "story.json")
    save_story_script(script, script_path)
    print(f"故事脚本生成完成: {script_path}")

    # 3. 生成场景图像
    for i, scene in enumerate(script["scenes"]):
        img_path = os.path.join(project_dir, f"scene_{i + 1}.png")
        generate_scene_image(scene["visual_description"], img_path)
        print(f"场景 {i + 1} 图像生成完成: {img_path}")

    # 4. 生成音频
    for i, scene in enumerate(script["scenes"]):
        # 旁白
        if scene.get("narration"):
            audio_path = os.path.join(project_dir, f"scene_{i + 1}_nar.wav")
            synthesize_speech(scene["narration"], audio_path, VOICE_MAPPING["旁白"])

        # 对话
        for j, dialog in enumerate(scene["dialogue"]):
            audio_path = os.path.join(project_dir, f"scene_{i + 1}_dia_{j + 1}.wav")
            voice = VOICE_MAPPING.get(dialog["character"], VOICE_MAPPING["旁白"])
            synthesize_speech(dialog["text"], audio_path, voice)

    print("所有音频生成完成")

    # 5. 合成视频
    video_path = compose_video(script, project_dir)
    print(f"视频合成完成: {video_path}")

    # 6. 发布到平台
    title = f"【成语动画】{idiom} - {animal_a}和{animal_b}的故事"
    description = f"改编自成语'{idiom}'的动画故事，寓教于乐，适合青少年观看"
    publish_results = publish_to_platforms(video_path, title, description)

    # 计算耗时
    elapsed = time.time() - start_time
    print(f"成语 '{idiom}' 处理完成! 耗时: {elapsed:.2f}秒")

    return {
        "idiom": idiom,
        "project_dir": project_dir,
        "video_path": video_path,
        "publish_results": publish_results,
        "processing_time": elapsed
    }


if __name__ == "__main__":
    # 加载成语列表
    idioms = load_idioms_from_csv("idioms.csv")

    # 处理所有成语
    results = []
    for idiom in idioms:
        results.append(process_idiom(idiom))

    # 生成汇总报告
    print("\n===== 处理完成 =====")
    for res in results:
        print(f"成语: {res['idiom']}, 视频: {res['video_path']}, 耗时: {res['processing_time']:.2f}秒")