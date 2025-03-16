import os
import sys
# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 返回上一级目录
parent_dir = os.path.dirname(current_dir)
# 将项目根目录添加到 sys.path 中
sys.path.append(parent_dir)
# 使用绝对导入
from config.config_loader import load_config

def combination(Part, drama):
    # print("0\n")
    try:
        config = load_config()
        Text_config = config["Text summaries"]
        # 修正引号使用问题
        input_folder_path = f'{config["PROCESS_FOLDER"]}/{Text_config["Text_1"]}/{Part}/{drama}'
        output_file = f'{config["PROCESS_FOLDER"]}/{Text_config["COMBINATION"]}/{drama}/{Part}.txt'
    except KeyError as e:
        print(f"配置文件中缺少必要的键: {e}")
        print("请检查 config.json 文件内容。")
        exit(1)

    # 初始化一个空字符串，用于存储所有文件的内容
    combined_content = ""
    
    # print("1\n")

    # 检查输入文件夹是否存在
    if not os.path.exists(input_folder_path):
        print(f"输入文件夹 {input_folder_path} 不存在。")
        return

    # 遍历文件夹中的所有文件
    for root, _, files in os.walk(input_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # 以只读模式打开文件，并使用 UTF-8 编码读取内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    # 直接读取文件全部内容
                    content = f.read()
                    # 检查字符数是否少于100，少于则跳过
                    if len(content) < 100:
                        continue
                    # 将当前文件的内容添加到合并内容中，并在后面添加换行符作为分割
                    combined_content += content + "\n"
            except Exception as e:
                print(f"处理文件 {file} 时出错: {e}")
                
    # print("2\n")

    # 如果合并内容不为空，去掉最后多余的换行符
    if combined_content:
        combined_content = combined_content.rstrip("\n")

    # 获取输出文件所在的目录
    output_dir = os.path.dirname(output_file)
    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 将合并后的内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(combined_content)

    print(f"文件合并完成，合并后的文件为: {output_file}")