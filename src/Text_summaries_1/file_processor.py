import os
import sys
from api_request import extract_features

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 返回上一级目录
parent_dir = os.path.dirname(current_dir)
# 将项目根目录添加到 sys.path 中
sys.path.append(parent_dir)
# 使用绝对导入
from config.config_loader import load_config

def format_features(features):
    output = "对于文本中主要人物的外貌特征：\n"
    output += f"  外貌特征：{', '.join(features)}\n"
    return output

def find_unprocessed_files(input_folder, output_folder):
    unprocessed_files = []
    for root, dirs, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        # 确保输出子文件夹存在
        os.makedirs(output_subfolder, exist_ok=True)
        for file in files:
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_subfolder, file)
            if not os.path.exists(output_file_path):
                unprocessed_files.append((input_file_path, output_file_path))
    return unprocessed_files

def process_file(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, input_file_path, output_file_path, encoding, Part, api_content):
    try:
        
        with open(input_file_path, 'r', encoding=encoding) as file:
            text = file.read()
        features = extract_features(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, text, api_content, Part)
        if features:
            # 只有在提取到信息时，才创建输出文件
            formatted_features = f"  {Part}信息：{', '.join(features)}\n"
            with open(output_file_path, 'w', encoding=encoding) as output_file:
                output_file.write(formatted_features)
            print(f"已处理并保存文件: {input_file_path} -> {output_file_path}")
        else:
            print(f"未提取到有效{Part}信息，跳过文件: {input_file_path}")
    except Exception as e:
        print(f"处理文件 {input_file_path} 时出现异常（类型: {type(e).__name__}）: {e}")

# 定义函数遍历文件夹，找出并处理尚未处理的文件
def traverse_folder(Part):
    try:
        config = load_config()
        if config is None:
            exit(1)
        parts = config["parts"]
        Text_config = config["Text summaries"]
        One_part = parts[Part]
        api_content = One_part["api_content"]
        input_file_path = config["photo_to_txt"]["OUTPUT_FOLDER"]
        output_file_path = f"{Text_config["Text_1"]}/{Part}"
        # 从 shared_config 中获取 API 相关配置
        shared_config = config["shared_config"]
        DEEPSEEK_API_URL = shared_config["DEEPSEEK_API_URL"]
        DEEPSEEK_API_KEY = shared_config["DEEPSEEK_API_KEY"]
        DEEPSEEK_MODEL = shared_config["DEEPSEEK_MODEL"]
        encoding = shared_config["encoding"]
    except KeyError as e:
        print(f"配置文件中缺少必要的键: {e}")
        print("请检查 config.json 文件内容。")
        exit(1)
    unprocessed_files = find_unprocessed_files(input_file_path, output_file_path)
    for input_file_path, output_file_path in unprocessed_files:
        output_dir = os.path.dirname(output_file_path)
        os.makedirs(output_dir, exist_ok=True)
        process_file(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, input_file_path, output_file_path, encoding, Part, api_content)
