import os
import re

directory = "./"  # 当前目录，可修改为目标文件夹路径

def parse_toml_front_matter(toml_text):
    """简单解析 TOML 风格 front matter"""
    data = {}
    # title = 'xxx'
    title_match = re.search(r"title\s*=\s*['\"](.*?)['\"]", toml_text)
    if title_match:
        data["title"] = title_match.group(1)
    # date = 2022-06-24T23:25:08+08:00
    date_match = re.search(r"date\s*=\s*(.*)", toml_text)
    if date_match:
        data["date"] = date_match.group(1).strip()
    # draft = false  忽略
    # category = 'xxx'
    category_match = re.search(r"category\s*=\s*['\"](.*?)['\"]", toml_text)
    if category_match:
        data["categories"] = [category_match.group(1)]
    else:
        data["categories"] = []
    # tags = ['a','b']
    tags_match = re.search(r"tags\s*=\s*\[(.*?)\]", toml_text)
    if tags_match:
        tags_str = tags_match.group(1)
        tags = [t.strip().strip("'\"") for t in tags_str.split(",") if t.strip()]
        data["tags"] = tags
    else:
        data["tags"] = []
    return data

def convert_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith("+++"):
        parts = content.split("+++", 2)
        if len(parts) >= 3:
            toml_text = parts[1].strip()
            body = parts[2].strip()

            data = parse_toml_front_matter(toml_text)

            # 构建 YAML front matter
            yaml_lines = ["---"]
            yaml_lines.append(f"title: {data['title']}")
            yaml_lines.append(f"date: {data['date']}")
            yaml_lines.append("tags:")
            for tag in data["tags"]:
                yaml_lines.append(f"- {tag}")
            yaml_lines.append("categories:")
            for cat in data["categories"]:
                yaml_lines.append(f"- {cat}")
            yaml_lines.append("---\n")

            new_content = "\n".join(yaml_lines) + body

            # 写回原文件
            with open(file_path, "w", encoding="utf-8") as out_f:
                out_f.write(new_content)
            print(f"Converted: {file_path}")
        else:
            print(f"Skipped (invalid TOML front matter): {file_path}")
    else:
        print(f"Skipped (no TOML front matter): {file_path}")

for filename in os.listdir(directory):
    if filename.endswith(".md"):
        convert_file(os.path.join(directory, filename))