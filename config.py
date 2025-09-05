import os

# 基础配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# API配置
DEEPSEEK_API_KEY = "sk-0fbcaf78abf7432294d0883b25b544f6"
DEEPSEEK_MODEL = "deepseek-chat"  # 根据实际模型调整

# 图像生成配置 (示例使用Stable Diffusion)
IMAGE_MODEL = "runwayml/stable-diffusion-v1-5"
IMAGE_SIZE = (512, 512)

# 语音合成配置 (示例使用Azure)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_REGION = "eastasia"
# 简化VOICE_MAPPING，只定义一个用于讲述故事的可爱音色，例如晓晓的友好风格
VOICE_MAPPING = {
    "storyteller": "zh-CN-XiaoxiaoNeural" # 这是一个常用且比较可爱的女声
}
# 其他配置保持不变...

# 视频配置
VIDEO_FPS = 24
SCENE_DURATION = 5  # 每个场景默认时长(秒)

# 平台发布配置 (示例)
PLATFORMS = ["douyin", "kuaishou", "bilibili"]