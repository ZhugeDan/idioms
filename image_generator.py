from diffusers import StableDiffusionPipeline
import torch
from config import IMAGE_MODEL, IMAGE_SIZE

# 全局加载模型 (避免重复加载)
pipe = None


def init_image_generator():
    """初始化图像生成器"""
    global pipe
    if pipe is None:
        pipe = StableDiffusionPipeline.from_pretrained(
            IMAGE_MODEL,
            torch_dtype=torch.float16
        )
        pipe = pipe.to("cuda")


def generate_scene_image(prompt, output_path):
    """生成单个场景图像"""
    global pipe
    if pipe is None:
        init_image_generator()

    image = pipe(
        prompt=prompt,
        height=IMAGE_SIZE[0],
        width=IMAGE_SIZE[1],
        num_inference_steps=25,
        guidance_scale=7.5
    ).images[0]

    image.save(output_path)
    return output_path