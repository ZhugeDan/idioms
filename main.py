import time
import logging
from idiom_processor import load_idioms_from_csv, create_project_folder
from story_generator import generate_story_script, save_story_script
from image_generator import generate_scene_image
from audio_generator import synthesize_speech
from video_composer import compose_video
from publisher import publish_to_platforms
from config import VOICE_MAPPING
import json
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("idiom_processing.log"),
        logging.StreamHandler()
    ]
)


def process_idiom(idiom, animal_a="大橘猫", animal_b="小兔子"):
    """处理单个成语的全流程"""
    logging.info(f"开始处理成语: {idiom}")
    start_time = time.time()

    try:
        # 1. 创建项目目录
        project_dir = create_project_folder(idiom)
        logging.info(f"项目目录: {project_dir}")

        # 2. 生成故事脚本
        script = generate_story_script(idiom, animal_a, animal_b)
        script_path = os.path.join(project_dir, "story.json")
        save_story_script(script, script_path)
        logging.info(f"故事脚本生成完成: {script_path}")

        # 3. 生成场景图像（添加错误处理）
        for i, scene in enumerate(script["scenes"]):
            try:
                img_path = os.path.join(project_dir, f"scene_{i + 1}.png")
                generate_scene_image(scene["visual_description"], img_path)
                logging.info(f"场景 {i + 1} 图像生成完成: {img_path}")
            except Exception as e:
                logging.error(f"生成场景 {i + 1} 图像失败: {str(e)}")
                continue

        # 4. 生成音频（添加错误处理）
        for i, scene in enumerate(script["scenes"]):
            try:
                if scene.get("narration"):
                    audio_path = os.path.join(project_dir, f"scene_{i + 1}_nar.wav")
                    synthesize_speech(scene["narration"], audio_path, VOICE_MAPPING["旁白"])

                for j, dialog in enumerate(scene["dialogue"]):
                    audio_path = os.path.join(project_dir, f"scene_{i + 1}_dia_{j + 1}.wav")
                    voice = VOICE_MAPPING.get(dialog["character"], VOICE_MAPPING["旁白"])
                    synthesize_speech(dialog["text"], audio_path, voice)
            except Exception as e:
                logging.error(f"生成场景 {i + 1} 音频失败: {str(e)}")
                continue

        logging.info("所有音频生成完成")

        # 5. 合成视频
        video_path = compose_video(script, project_dir)
        logging.info(f"视频合成完成: {video_path}")

        # 6. 发布到平台
        title = f"【成语动画】{idiom} - {animal_a}和{animal_b}的故事"
        description = f"改编自成语'{idiom}'的动画故事，寓教于乐，适合青少年观看"
        publish_results = publish_to_platforms(video_path, title, description)

        # 计算耗时
        elapsed = time.time() - start_time
        logging.info(f"成语 '{idiom}' 处理完成! 耗时: {elapsed:.2f}秒")

        return {
            "idiom": idiom,
            "project_dir": project_dir,
            "video_path": video_path,
            "publish_results": publish_results,
            "processing_time": elapsed
        }

    except Exception as e:
        logging.error(f"处理成语 '{idiom}' 时发生严重错误: {str(e)}")
        return None


if __name__ == "__main__":
    try:
        # 加载成语列表
        idioms = load_idioms_from_csv("idioms.csv")
        logging.info(f"成功加载 {len(idioms)} 个成语")

        # 处理所有成语
        results = []
        for idiom in idioms:
            result = process_idiom(idiom)
            if result:
                results.append(result)

        # 生成汇总报告
        logging.info("\n===== 处理完成 =====")
        for res in results:
            logging.info(f"成语: {res['idiom']}, 视频: {res['video_path']}, 耗时: {res['processing_time']:.2f}秒")

    except Exception as e:
        logging.error(f"程序执行失败: {str(e)}")