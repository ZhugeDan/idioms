import re
from bs4 import BeautifulSoup  # 用于处理可能存在的HTML标签


def extract_idiom_stories(text):
    """
    从文档文本中提取成语故事数据
    返回包含(成语名, 故事内容)的元组列表
    """
    # 用正则分割成语条目（###开头作为分隔）
    entries = re.split(r'###\s+', text)[1:]
    idiom_data = []

    for entry in entries:
        # 分离成语名和内容（第一个换行符前是成语名）
        parts = entry.split('\n', 1)
        if len(parts) < 2:
            continue

        idiom_name = parts[0].strip()
        # 清理故事内容中的HTML标签和多余空格
        content = BeautifulSoup(parts[1], 'html.parser').get_text().strip()
        idiom_data.append((idiom_name, content))

    return idiom_data


def generate_html_table(idiom_data):
    """生成包含三列的HTML表格（序号、成语名、故事）"""
    html = [
        '<table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%;">',
        '<thead><tr>',
        '<th style="width: 5%">序号</th>',
        '<th style="width: 15%">成语名称</th>',
        '<th>故事内容</th>',
        '</tr></thead><tbody>'
    ]

    for idx, (name, story) in enumerate(idiom_data, 1):
        # 将故事内容中的换行符转换为HTML换行标签
        formatted_story = story.replace('\n', '<br>')
        html.append(f'<tr><td>{idx}</td><td>{name}</td><td>{formatted_story}</td></tr>')

    html.append('</tbody></table>')
    return '\n'.join(html)


# 示例使用
if __name__ == "__main__":
    with open('中华成语故事.txt', 'r', encoding='utf-8') as f:
        document_text = f.read()

    # 提取数据
    idiom_data = extract_idiom_stories(document_text)
    # 生成HTML表格
    html_table = generate_html_table(idiom_data)

    # 输出到文件
    with open('成语故事表格.html', 'w', encoding='utf-8') as f:
        f.write(html_table)
    print("转换完成！输出文件：成语故事表格.html")