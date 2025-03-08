import os
import requests
import json
import time

# 从 config.json 文件中加载配置
def load_config():
    try:
        # 获取当前文件所在目录的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建 config.json 文件的完整路径
        config_path = os.path.join(current_dir, '..', 'config', 'config.json')
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
except KeyError as e:
    print(f"配置文件中缺少必要的键: {e}")
    print("请检查 config.json 文件内容。")
    exit(1)

# 从 Text summaries 中获取输入输出文件夹配置
try:
    text_summaries_config = config["Text summaries"]
    INPUT_FOLDER = text_summaries_config["INPUT_FOLDER"]
    OUTPUT_FOLDER = text_summaries_config["OUTPUT_FOLDER"]
except KeyError as e:
    print(f"配置文件中缺少必要的键: {e}")
    print("请检查 config.json 文件内容。")
    exit(1)

# 定义请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
}

# 定义函数从文本中提取主要人物及其所有可能的名称
def extract_main_characters(text):
    messages = [
        {
            "role": "user",
            "content": f"请提取以下文本中每个人物的所有可能名称，以人物为单位列出，格式为人物标准名称:别名1,别名2,... 。示例：张三:小张,三哥 。文本：{text}"
        }
    ]
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": messages
    }
    max_retries = 5  # 最大重试次数
    retry_delay = 5  # 每次重试的延迟时间（秒）
    for attempt in range(max_retries):
        print(f"正在向 DeepSeek API 发起提取主要人物名称请求（第 {attempt + 1} 次尝试）...")
        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            characters_str = result["choices"][0]["message"]["content"]
            character_mapping = {}
            for line in characters_str.splitlines():
                if ':' in line:
                    main_name, aliases = line.split(':')
                    all_names = [main_name] + aliases.split(',')
                    for name in all_names:
                        character_mapping[name] = main_name
            print("成功从 DeepSeek API 获取到主要人物名称映射。")
            return character_mapping
        except requests.HTTPError as e:
            if e.response.status_code == 429:
                print(f"请求频率过高，将在 {retry_delay} 秒后重试（第 {attempt + 1} 次尝试）...")
                time.sleep(retry_delay)
            else:
                print(f"请求 DeepSeek API 时出错: {e}")
                break
        except requests.RequestException as e:
            print(f"请求 DeepSeek API 时出错: {e}")
            break
    print("达到最大重试次数，请求失败。")
    return {}

# 定义函数从文本中提取总结信息
def extract_summary(text):
    messages = [
        {
            "role": "user",
            "content": f"请总结以下文本中的主要人物、人物性格、外貌形象、发生的事件、出现的人物话语、口头禅：{text}"
        }
    ]
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": messages
    }
    max_retries = 5  # 最大重试次数
    retry_delay = 5  # 每次重试的延迟时间（秒）
    for attempt in range(max_retries):
        print(f"正在向 DeepSeek API 发起请求（第 {attempt + 1} 次尝试）...")
        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            summary = result["choices"][0]["message"]["content"]
            print("成功从 DeepSeek API 获取到响应。")
            return summary
        except requests.HTTPError as e:
            if e.response.status_code == 429:
                print(f"请求频率过高，将在 {retry_delay} 秒后重试（第 {attempt + 1} 次尝试）...")
                time.sleep(retry_delay)
            else:
                print(f"请求 DeepSeek API 时出错: {e}")
                break
        except requests.RequestException as e:
            print(f"请求 DeepSeek API 时出错: {e}")
            break
    print("达到最大重试次数，请求失败。")
    return None

# 审查并修正总结信息中的人物名称
def review_and_fix_summary(summary, character_mapping):
    for alias, main_name in character_mapping.items():
        summary = summary.replace(alias, main_name)
    return summary

# 整理总结信息为指定格式
def format_summary(summary, character_mapping):
    characters_info = {}
    all_events = []
    all_dialogues = []

    # 简单解析总结信息，这里可以根据实际 API 返回格式调整
    lines = summary.splitlines()
    current_character = None
    for line in lines:
        if any(name in line for name in character_mapping.values()):
            for name in character_mapping.values():
                if name in line:
                    current_character = name
                    if current_character not in characters_info:
                        characters_info[current_character] = {
                            "姓名": current_character,
                            "外貌": "",
                            "性格": "",
                            "经历事件": [],
                            "口头禅": ""
                        }
                    break
        elif "外貌" in line:
            if current_character:
                characters_info[current_character]["外貌"] = line.replace("外貌:", "").strip()
        elif "性格" in line:
            if current_character:
                characters_info[current_character]["性格"] = line.replace("性格:", "").strip()
        elif "事件" in line:
            if current_character:
                event = line.replace("事件:", "").strip()
                characters_info[current_character]["经历事件"].append(event)
                all_events.append(event)
        elif "口头禅" in line:
            if current_character:
                characters_info[current_character]["口头禅"] = line.replace("口头禅:", "").strip()
        elif "话语" in line:
            dialogue = line.replace("话语:", "").strip()
            all_dialogues.append(dialogue)

    # 构建最终输出字符串
    output = ""
    for character, info in characters_info.items():
        output += f"对于每个角色：\n"
        output += f"  姓名：{info['姓名']}\n"
        output += f"  外貌：{info['外貌']}\n"
        output += f"  性格：{info['性格']}\n"
        output += f"  经历事件：{', '.join(info['经历事件'])}\n"
        output += f"  口头禅：{info['口头禅']}\n\n"

    output += "对于文本汇总发生的事件：\n"
    output += f"  发生的事件：{', '.join(all_events)}\n\n"

    output += "汇总人物话语：\n"
    output += f"  人物话语：{', '.join(all_dialogues)}\n"

    return output

# 定义函数处理单个文件
def process_file(input_file_path, output_file_path):
    try:
        encoding = shared_config["encoding"]
        with open(input_file_path, 'r', encoding=encoding) as file:
            text = file.read()
        # 提取主要人物及其所有可能的名称
        character_mapping = extract_main_characters(text)
        summary = extract_summary(text)
        if summary and summary.strip():
            # 审查并修正总结信息中的人物名称
            fixed_summary = review_and_fix_summary(summary, character_mapping)
            # 整理总结信息为指定格式
            formatted_summary = format_summary(fixed_summary, character_mapping)
            with open(output_file_path, 'w', encoding=encoding) as output_file:
                output_file.write(formatted_summary)
            print(f"已处理并保存文件: {input_file_path} -> {output_file_path}")
        else:
            print(f"未提取到有效信息，跳过文件: {input_file_path}")
    except Exception as e:
        print(f"处理文件 {input_file_path} 时出错: {e}")

# 找出还未处理的文件
def find_unprocessed_files(input_folder, output_folder):
    unprocessed_files = []
    for root, dirs, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        for file in files:
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_subfolder, file)
            if not os.path.exists(output_file_path):
                unprocessed_files.append((input_file_path, output_file_path))
    return unprocessed_files

# 定义函数遍历文件夹
def traverse_folder(input_folder, output_folder):
    unprocessed_files = find_unprocessed_files(input_folder, output_folder)
    for input_file_path, output_file_path in unprocessed_files:
        output_dir = os.path.dirname(output_file_path)
        os.makedirs(output_dir, exist_ok=True)
        process_file(input_file_path, output_file_path)

if __name__ == "__main__":
    traverse_folder(INPUT_FOLDER, OUTPUT_FOLDER)