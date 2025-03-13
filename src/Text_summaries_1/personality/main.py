import os
from config_loader import load_config
from file_processor import process_file, find_unprocessed_files

# 加载配置
config = load_config()
if config is None:
    exit(1)

try:
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

# 从 Text summaries 中获取输入输出文件夹配置
try:
    text_summaries_config = config["Text summaries"]
    INPUT_FOLDER = text_summaries_config["INPUT_FOLDER"]
    OUTPUT_FOLDER = text_summaries_config["PERSONALITY_OUTPUT_FOLDER"]
except KeyError as e:
    print(f"配置文件中缺少必要的键: {e}")
    print("请检查 config.json 文件内容。")
    exit(1)

# 定义函数遍历文件夹，找出并处理尚未处理的文件
def traverse_folder(input_folder, output_folder):
    unprocessed_files = find_unprocessed_files(input_folder, output_folder)
    for input_file_path, output_file_path in unprocessed_files:
        output_dir = os.path.dirname(output_file_path)
        os.makedirs(output_dir, exist_ok=True)
        process_file(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, input_file_path, output_file_path, encoding)

if __name__ == "__main__":
    traverse_folder(INPUT_FOLDER, OUTPUT_FOLDER)