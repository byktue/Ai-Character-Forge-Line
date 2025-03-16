import os
import sys
import json
import pdfplumber

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 返回上一级目录
parent_dir = os.path.dirname(current_dir)
# 将项目根目录添加到 sys.path 中
sys.path.append(parent_dir)
# 使用绝对导入
from config.config_loader import load_config

# ================== 从 PDF 提取文本函数 ==================
def extract_text_from_pdf(pdf_path):
    """从 PDF 文件中提取文本并处理段落"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                all_text += page_text

            # 处理段落
            paragraphs = []
            current_paragraph = ""
            lines = all_text.splitlines()
            for line in lines:
                if line.strip():  # 如果当前行不为空
                    current_paragraph += line.strip() + " "
                else:
                    if current_paragraph:
                        paragraphs.append(current_paragraph.strip())
                        current_paragraph = ""

            # 处理最后一个段落
            if current_paragraph:
                paragraphs.append(current_paragraph.strip())

            final_text = "\n".join(paragraphs)
            return final_text
    except Exception as e:
        print(f"处理 PDF 文件 {pdf_path} 时出错: {str(e)}")
        return ""

# ================== 处理文件夹函数 ==================
def process_folder(input_root, output_root):
    """递归处理文件夹结构"""
    for root, dirs, files in os.walk(input_root):
        # 创建对应的输出目录
        relative_path = os.path.relpath(root, input_root)
        output_dir = os.path.join(output_root, relative_path)

        # 检查输出目录是否已经存在
        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            print(f"跳过已存在的输出目录: {output_dir}")
            continue

        os.makedirs(output_dir, exist_ok=True)

        # 处理文件
        for file in files:
            if file.lower().endswith('.pdf'):
                input_path = os.path.join(root, file)
                # 生成输出路径
                filename = os.path.splitext(file)[0] + '.txt'
                output_path = os.path.join(output_dir, filename)

                # 检查输出文件是否存在且非空
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    print(f"跳过已存在且非空的文件: {output_path}")
                    continue

                # 提取文字
                text = extract_text_from_pdf(input_path)
                # 保存文本
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"已处理：{input_path} -> {output_path}")

    # 检查并删除空的输出子文件夹
    for root, dirs, files in os.walk(output_root, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"已删除空文件夹: {dir_path}")

def pdf_to_txt(Drama):
    
    config = load_config()
    
    INPUT_FOLDER = f"{config["INPUT_FOLDER"]}/{Drama}"
    OUTPUT_FOLDER = f"{config["PROCESS_FOLDER"]}/{config["photo_to_txt"]["OUTPUT_FOLDER"]}/{Drama}"
    # 创建输入目录（如果不存在）
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"已创建输入目录: {INPUT_FOLDER}")

    # 创建输出目录（自动创建多级目录）
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # 显示最终使用的路径
    print(f"📂 输入目录: {os.path.abspath(INPUT_FOLDER)}")
    print(f"📂 输出目录: {os.path.abspath(OUTPUT_FOLDER)}")

    # 开始处理
    print("\n=== 开始处理 PDF 文件 ===")
    process_folder(INPUT_FOLDER, OUTPUT_FOLDER)
    print("=== 处理完成 ===")


# ================== 主程序入口 ==================
if __name__ == "__main__":
    pdf_to_txt("归途七万里")