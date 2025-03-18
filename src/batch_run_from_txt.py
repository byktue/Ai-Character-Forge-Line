import os
import json
from run_one import run_one

# 定义读取txt文件并批量运行程序的函数
def batch_run_from_txt(file_path):
    try:
        # 打开txt文件
        with open(file_path, 'r', encoding='utf-8') as file:
            # 逐行读取文件内容
            for line in file:
                # 去除行尾的换行符..
                line = line.strip()
                # 如果行为空，跳过该行
                if not line:
                    continue
                # 按空格分割行内容，提取DRAMA和AVATAR信息
                parts = line.split()
                if len(parts) >= 2:
                    drama = parts[0]
                    avatar = parts[1]
                    # 调用封装好的程序
                    run_one(drama, avatar)
                else:
                    print(f"格式错误: {line}")
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")



if __name__ == "__main__":
    
    # 获取当前文件所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 config.json 文件的完整路径
    config_path = os.path.join(current_dir, 'config', 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("未找到 config.json 文件，请检查文件是否存在。")
        exit(1)
    except json.JSONDecodeError:
        print("config.json 文件格式错误，请检查文件内容。")
        exit(1)
    
    # 指定txt文件的路径
    txt_file_path = config["INPUT_LIST"]

    # 调用函数进行批量运行
    batch_run_from_txt(txt_file_path)