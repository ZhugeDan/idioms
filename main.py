import time
import logging
from idiom_processor import load_idioms_from_csv, create_project_folder
from story_generator import generate_story_script, save_story_text  # 注意：改为save_story_text
from image_generator import generate_scene_image
from audio_generator import synthesize_speech
from video_composer import compose_video  # 可能需要调整此导入
from config import VOICE_MAPPING
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


def process_idiom(idiom):
    """
    处理单个成语的全流程：生成故事文本、朗读、生成配图、合成视频
    参数:
        idiom: 要处理的成语
    返回:
        包含处理结果的字典，出错时返回None
    """
    logging.info(f"开始处理成语: {idiom}")
    start_time = time.time()

    try:
        # 1. 创建项目目录
        project_dir = create_project_folder(idiom)
        logging.info(f"项目目录: {project_dir}")

        # 2. 生成故事文本 (调用修改后的函数，返回字符串)
        story_text = generate_story_script(idiom)  # 不再需要animal_a, animal_b参数
        if not story_text:
            logging.error(f"生成成语 {idiom} 的故事文本失败，跳过处理。")
            return None

        text_path = os.path.join(project_dir, "story.txt")
        save_story_text(story_text, text_path)  # 使用新的保存文本函数
        logging.info(f"故事文本已保存: {text_path}")

        # 3. 生成音频 (整个故事一个音频文件)
        audio_path = os.path.join(project_dir, "full_story_narration.wav")
        # 使用配置中的“旁白”或“讲故事者”音色
        synthesize_speech(story_text, audio_path, VOICE_MAPPING.get("旁白"))
        logging.info(f"故事音频已生成: {audio_path}")

        # 4. 生成图像 (根据整个故事生成一张代表性图片)
        # 构建图像提示词 - 结合成语和故事开头部分
        image_prompt = f"卡通风格，成语'{idiom}'的插画，表现其故事内容：{story_text[:150]}..."
        image_path = os.path.join(project_dir, "main_illustration.png")
        generate_scene_image(image_prompt, image_path)
        logging.info(f故事插图已生成: {image_path} ")

        # 5. 合成视频 (单张图片配整个故事的音频)
        # 注意：需要确保compose_video函数已适配新的参数（单图单音频）
        video_path = compose_video(story_text, project_dir, image_path, audio_path)
        logging.info(f"视频合成完成: {video_path}")

        # 6. （可选）发布到平台 - 可根据需要保留或注释掉
        # title = f"【成语故事】{idiom}"
        # description = f"生动讲解成语'{idiom}'的故事，寓教于乐"
        # publish_results = publish_to_platforms(video_path, title, description)

        # 计算耗时
        elapsed_time = time.time() - start_time
        logging.info(f"成语 '{idiom}' 处理完成! 耗时: {elapsed_time:.2f}秒")

        return {
            "idiom": idiom,
            "project_dir": project_dir,
            "text_path": text_path,
            "audio_path": audio_path,
            "image_path": image_path,
            "video_path": video_path,
            "processing_time": elapsed_time
        }

    except Exception as e:
        logging.error(f"处理成语 '{idiom}' 时发生错误: {str(e)}", exc_info=True)
        return None


if __name__ == "__main__":
    """
    主程序入口点。当此脚本被直接运行时，__name__ 的值为 '__main__'，以下代码块将被执行。
    如果此脚本被作为模块导入，则以下代码不会运行。[1,2,3](@ref)
    """
    try:
        # 加载成语列表
        idioms = load_idioms_from_csv("idioms.csv")
        logging.info(f"成功加载 {len(idioms)} 个成语")

        # 处理所有成语
        results = []
        for idiom in idioms:
            result = process_idiom(idiom)  # 调用新的处理函数
            if result:
                results.append(result)
            # 可选：在每个成语处理后添加短暂停顿，避免请求过于频繁
            # time.sleep(1)

        # 生成汇总报告
        logging.info("\n===== 批量处理完成 =====")
        successful_count = len(results)
        failed_count = len(idioms) - successful_count
        logging.info(f"总计处理: {len(idioms)} 个成语")
        logging.info(f"成功: {successful_count} 个")
        logging.info(f"失败: {failed_count} 个")

        if results:
            total_time = sum(res['processing_time'] for res in results)
            avg_time = total_time / successful_count if successful_count > 0 else 0
            logging.info(f"总耗时: {total_time:.2f} 秒, 平均每个成语耗时: {avg_time:.2f} 秒")

            # 打印每个成功处理的成语信息
            for res in results:
                logging.info(f"成语 '{res['idiom']}': 视频文件 -> {res['video_path']}")

    except FileNotFoundError:
        logging.error("未找到成语列表文件 'idioms.csv'，请确保文件存在且格式正确。")
    except Exception as e:
        logging.error(f"主程序执行过程中发生未预期错误: {str(e)}", exc_info=True)