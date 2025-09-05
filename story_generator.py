import json
import requests
from config import DEEPSEEK_API_KEY, DEEPSEEK_MODEL


def generate_story_script(idiom, animal_a, animal_b):
    """调用DeepSeek API生成故事脚本"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    你是一个经验丰富的儿童故事作家。请将成语【{idiom}】改编成一个适合制作3分钟动画短片的剧本，用青少年喜欢看的形式展示出来】。

    输出要求：
    1. 严格使用JSON格式
    2. 包含字段: title, logline, scenes
    3. 每个scene包含: scene_number, visual_description, dialogue, narration
    4. 对话格式: [{"character": "角色名", "text": "对话内容"}]
    """

    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000,
        "response_format": {"type": "json_object"}
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def save_story_script(script, output_path):
    """保存故事脚本到文件"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(script, f, indent=2, ensure_ascii=False)