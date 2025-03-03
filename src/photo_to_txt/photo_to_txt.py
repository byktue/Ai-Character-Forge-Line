import os
import json
import pdfplumber

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
        os.makedirs(output_dir, exist_ok=True)

        # 处理文件
        for file in files:
            if file.lower().endswith('.pdf'):
                input_path = os.path.join(root, file)
                # 提取文字
                text = extract_text_from_pdf(input_path)
                # 生成输出路径
                filename = os.path.splitext(file)[0] + '.txt'
                output_path = os.path.join(output_dir, filename)
                # 保存文本
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"已处理：{input_path} -> {output_path}")

# ================== 配置管理模块 ==================
def load_config():
    """加载配置文件并返回路径配置"""
    # 设置默认配置（当配置文件不存在时使用）
    default_config = {
        "INPUT_FOLDER": "input_pdfs",
        "OUTPUT_FOLDER": "output_texts"
    }

    try:
        # 获取配置文件路径（支持跨文件夹）
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
        config_path = os.path.join(config_dir, 'config.json')

        # 尝试读取配置文件
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            print("⚠️ 未找到配置文件，使用默认路径")
            config = default_config

        # 获取配置值（带错误处理）
        input_path = config.get('INPUT_FOLDER', 'input_pdfs')
        output_path = config.get('OUTPUT_FOLDER', 'output_texts')

        # 路径标准化处理
        return (
            os.path.normpath(input_path),
            os.path.normpath(output_path)
        )
    except Exception as e:
        print(f"❌ 配置读取失败: {str(e)}，使用默认路径")
        return 'input_pdfs', 'output_texts'

# ================== 主程序入口 ==================
if __name__ == "__main__":
    # 加载配置
    INPUT_FOLDER, OUTPUT_FOLDER = load_config()

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