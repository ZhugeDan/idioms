import os
import pandas as pd
from config import OUTPUT_DIR

def load_idioms_from_csv(csv_path):
    """从CSV加载成语列表"""
    df = pd.read_csv(csv_path)
    return df["成语"].tolist()

def create_project_folder(idiom):
    """为每个成语创建项目文件夹"""
    project_dir = os.path.join(OUTPUT_DIR, idiom)
    os.makedirs(project_dir, exist_ok=True)
    return project_dir