import os
import time
from config_loader import load_config
from combination import combination

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
    APPEARANCE_OUTPUT_FOLDER = text_summaries_config["APPEARANCE_OUTPUT_FOLDER"]
    EVENTS_OUTPUT_FOLDER = text_summaries_config["EVENTS_OUTPUT_FOLDER"]
    IDENTITY_OUTPUT_FOLDER = text_summaries_config["IDENTITY_OUTPUT_FOLDER"]
    NAME_OUTPUT_FOLDER = text_summaries_config["NAME_OUTPUT_FOLDER"]
    PERSONALITY_OUTPUT_FOLDER = text_summaries_config["PERSONALITY_OUTPUT_FOLDER"]
    UTTERANCE_OUTPUT_FOLDER = text_summaries_config["UTTERANCE_OUTPUT_FOLDER"]

    COMBINATION = text_summaries_config["COMBINATION"]
    
except KeyError as e:
    print(f"配置文件中缺少必要的键: {e}")
    print("请检查 config.json 文件内容。")
    exit(1)

output_folder_mapping = {
    "APPEARANCE": APPEARANCE_OUTPUT_FOLDER,
    "EVENTS": EVENTS_OUTPUT_FOLDER,
    "IDENTITY": IDENTITY_OUTPUT_FOLDER,
    "NAME": NAME_OUTPUT_FOLDER,
    "PERSONALITY": PERSONALITY_OUTPUT_FOLDER,
    "UTTERANCE": UTTERANCE_OUTPUT_FOLDER
}

def one_part_sum(PART):
    INPUT_FOLDER = output_folder_mapping.get(PART)
    PART_COMBINATION = os.path.join(COMBINATION, f"{PART}.txt")
    combination(INPUT_FOLDER, PART_COMBINATION)
    time.sleep(10)  # 每次处理完一个文件后等待 10 秒
    return None

if __name__ == "__main__":
    one_part_sum("APPEARANCE")
    one_part_sum("EVENTS")
    one_part_sum("IDENTITY")
    one_part_sum("NAME")
    one_part_sum("PERSONALITY")
    one_part_sum("UTTERANCE")