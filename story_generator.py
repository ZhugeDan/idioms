import json
import requests
from config import DEEPSEEK_API_KEY, DEEPSEEK_MODEL


def generate_story_script(idiom):
    """调用DeepSeek API生成成语故事文本"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
你是一个讲故事的专家，擅长为青少年创作生动有趣的成语故事。请根据成语【{idiom}】，创作一个简短精彩的故事段落。

**要求：**
1.  **故事内容**：情节完整，生动有趣，能体现成语的核心寓意，适合青少年聆听。
2.  **输出格式**：直接输出**纯文本**，不要使用任何JSON、XML等结构化格式。不要包含“标题”、“旁白”、“对话”等字段标签。
3.  **语言风格**：语言口语化，流畅自然，适合用可爱亲切的声音朗读出来。
4.  **长度**：控制在200-300字左右，确保朗读时长在1-2分钟内。

请开始创作关于成语【{idiom}】的故事：
    """

    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000, # 根据故事长度调整
        # 注意：由于不再要求返回JSON，移除了 "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        response_data = response.json()
        story_text = response_data["choices"][0]["message"]["content"].strip() # 获取纯文本故事
        print(f"[DEBUG] 生成的故事文本: {story_text}")
        return story_text # 现在返回的是字符串，而不是字典

    except Exception as e:
        print(f"[ERROR] 生成故事文本时出错: {e}")
        return None

def save_story_text(story_text, output_path):
    """保存故事文本到文件"""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(story_text)
        print(f"[INFO] 故事文本已保存: {output_path}")
    except IOError as e:
        print(f"[ERROR] 文件保存失败: {e}")