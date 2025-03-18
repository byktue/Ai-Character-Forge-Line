import os
import json
from local_preprocessing.photo_to_txt import pdf_to_txt
from Text_summaries_1.main import Text_1_main
from Text_summaries_2.main import combination_main
from Text_summaries_3.main import final_output

def run_one(DRAMA, AVATAR):
    # 获取当前文件所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 config.json 文件的完整路径
    config_path = os.path.join(current_dir, 'config', 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("未找到 config.json 文件，请检查文件是否存在。")
        return
    except json.JSONDecodeError:
        print("config.json 文件格式错误，请检查文件内容。")
        return

    # pdf转txt
    # 检测输出是否已经存在
    path = f"{config['PROCESS_FOLDER']}/{config['photo_to_txt']['OUTPUT_FOLDER']}/{DRAMA}"
    if not os.path.exists(path):
        pdf_to_txt(DRAMA)

    # 剧本文本降维并总结
    # 检测输出是否已经存在
    path = f"{config['PROCESS_FOLDER']}/{config['Text summaries']['COMBINATION']}/{DRAMA}"
    if not os.path.exists(path):
        for _ in range(3):
            Text_1_main(DRAMA)
        combination_main(DRAMA)

    if AVATAR is not None:
        # 人设生成
        path = f"{config['OUTPUT_FOLDER']}/{DRAMA}/{AVATAR}"
        if not os.path.exists(path):
            final_output(DRAMA, AVATAR)

    return None

if __name__ == "__main__":
    DRAMA = "归途七万里"
    AVATAR = "张眷信"
    run_one(DRAMA, AVATAR)