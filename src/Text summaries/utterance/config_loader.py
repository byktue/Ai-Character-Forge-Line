import os
import json


def load_config():
    try:
        # 获取当前文件所在目录的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 获取项目根目录的绝对路径（假设项目根目录是包含 src 目录的上一级目录）
        project_root = os.path.dirname(current_dir)
        # 多获取一次所在目录的根目录
        super_project_root = os.path.dirname(project_root)
        # 构建 config.json 文件的完整路径
        config_path = os.path.join(super_project_root, 'config', 'config.json')
        print(f"尝试读取的 config.json 文件路径: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print("未找到 config.json 文件，请检查文件是否存在。")
        return None
    except json.JSONDecodeError:
        print("config.json 文件格式错误，请检查文件内容。")
        return None