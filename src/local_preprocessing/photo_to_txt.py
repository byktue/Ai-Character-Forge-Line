import os
import sys
import glob
import pdfplumber
import re
from datetime import datetime
import pytesseract
from PIL import Image

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config.config_loader import load_config

def clean_page_text(text):
    """增强型文本清洗"""
    # 移除分页标记（兼容多空格情况）
    text = re.sub(r'=+\s*Page\s*\d+\s*=+', '', text)
    # 移除孤立的数字行（保留选项编号）
    text = re.sub(r'(?<!\d\.)\n\d+\n', '\n', text)
    return text.strip()

def detect_special_paragraphs(lines):
    """处理特殊内容结构"""
    paragraphs = []
    current_para = []
    in_poem = False  # 诗歌模式标志

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 检测诗歌起始
        if not in_poem and re.search(r'[《》（）]', stripped):
            in_poem = True
            current_para = [stripped]
            continue

        # 处理诗歌内容
        if in_poem:
            if stripped.endswith(('。', '”')) or re.search(r'[》]$', stripped):
                paragraphs.append(' '.join(current_para))
                current_para = []
                in_poem = False
            else:
                current_para.append(stripped)
            continue

        # 选项检测（1. 或 •）
        if re.match(r'^(\d+\.|•)\s*', stripped):
            if current_para:
                paragraphs.append(' '.join(current_para))
            current_para = [stripped]
            continue

        # 常规段落处理
        if stripped:
            # 合并短行（小于15字符视为标题行）
            if current_para and len(current_para[-1]) < 15 and len(stripped) > 15:
                paragraphs.append(' '.join(current_para))
                current_para = [stripped]
            else:
                current_para.append(stripped)
        elif current_para:
            paragraphs.append(' '.join(current_para))
            current_para = []

    if current_para:
        paragraphs.append(' '.join(current_para))

    return paragraphs

def extract_text_from_pdf(pdf_path):
    """最终版PDF解析器"""
    try:
        all_paragraphs = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # 尝试常规文本提取
                text = page.extract_text(
                    x_tolerance=4,
                    y_tolerance=3,
                    layout=True,
                    extra_attrs=["fontname", "size"],
                    use_text_flow=True
                )

                if text:
                    # 调试输出原始内容
                    print(f"\n=== 原始页面内容 [P{page.page_number}] ===")
                    print(text[:500] + ("..." if len(text) > 500 else ""))

                    # 执行清洗和解析
                    cleaned = clean_page_text(text)
                    lines = [ln.strip() for ln in cleaned.splitlines() if ln.strip()]
                    paragraphs = detect_special_paragraphs(lines)
                else:
                    # 若常规提取失败，尝试 OCR
                    image = page.to_image()
                    image_path = f"page_{page.page_number}.png"
                    image.save(image_path)
                    text = pytesseract.image_to_string(Image.open(image_path))
                    os.remove(image_path)

                    # 调试输出原始内容
                    print(f"\n=== 原始页面内容 [P{page.page_number}] ===")
                    print(text[:500] + ("..." if len(text) > 500 else ""))

                    # 执行清洗和解析
                    cleaned = clean_page_text(text)
                    lines = [ln.strip() for ln in cleaned.splitlines() if ln.strip()]
                    paragraphs = detect_special_paragraphs(lines)

                # 记录结果
                all_paragraphs.extend(paragraphs)

                # 调试输出解析结果
                print(f"\n解析出 {len(paragraphs)} 个段落:")
                for idx, p in enumerate(paragraphs[:3], 1):
                    print(f"[段{idx}] {p[:60]}...")
                if len(paragraphs) > 3:
                    print(f"...（其余{len(paragraphs) - 3}个段落已省略）")

        return all_paragraphs if all_paragraphs else ["（内容解析失败）"]

    except Exception as e:
        print(f"\n❌ 解析异常: {str(e)}")
        return []

def should_skip_processing(input_path, output_dir, base_name, chunk_size):
    """改进的跳过逻辑，准确判断文件状态"""
    try:
        # 获取文件状态信息
        pdf_mtime = os.path.getmtime(input_path)
        expected_pattern = os.path.join(output_dir, f"{base_name}_part_*.txt")
        existing_files = glob.glob(expected_pattern)

        # 存在性检查
        if not existing_files:
            return False

        # 时间戳和有效性检查
        newest_pdf_time = pdf_mtime
        oldest_output_time = min((os.path.getmtime(f) for f in existing_files), default=0)

        # 主逻辑判断
        return all([
            all(os.path.getsize(f) > 0 for f in existing_files),  # 所有文件非空
            len(existing_files) >= 1,  # 至少存在一个文件
            oldest_output_time > newest_pdf_time  # 输出文件比PDF新
        ])
    except Exception as e:
        print(f"跳过检查出错: {str(e)}")
        return False

def process_folder(input_root, output_root, chunk_size=500):
    """增强的文件处理流程"""
    # 创建日志目录
    log_dir = os.path.join(output_root, "_processing_logs")
    os.makedirs(log_dir, exist_ok=True)

    for root, dirs, files in os.walk(input_root):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        relative_path = os.path.relpath(root, input_root)
        output_dir = os.path.join(output_root, relative_path)
        os.makedirs(output_dir, exist_ok=True)

        for file in files:
            if not file.lower().endswith('.pdf'):
                continue

            # 创建每个文件的日志记录
            log_file = os.path.join(log_dir, f"{datetime.now():%Y%m%d}.log")
            input_path = os.path.join(root, file)
            base_name = os.path.splitext(file)[0]

            # 跳过检查
            if should_skip_processing(input_path, output_dir, base_name, chunk_size):
                print(f"⇢ 跳过已处理文件: {file}")
                with open(log_file, "a", encoding="utf-8") as log:
                    log.write(f"[SKIP] {datetime.now():%Y-%m-%d %H:%M:%S} {file}\n")
                continue

            # 执行文本提取
            try:
                paragraphs = extract_text_from_pdf(input_path)
                if not paragraphs:
                    print(f"⇢ 内容提取失败: {file}")
                    with open(log_file, "a", encoding="utf-8") as log:
                        log.write(f"[FAIL] {datetime.now():%Y-%m-%d %H:%M:%S} {file}\n")
                    continue

                # 清理旧文件
                for old_file in glob.glob(os.path.join(output_dir, f"{base_name}_part_*.txt")):
                    try:
                        os.remove(old_file)
                    except Exception as e:
                        print(f"⇢ 文件清理失败: {old_file} - {str(e)}")

                # 分块写入
                for i in range(0, len(paragraphs), chunk_size):
                    chunk_number = (i // chunk_size) + 1
                    output_path = os.path.join(output_dir, f"{base_name}_part_{chunk_number:03d}.txt")

                    # 确保写入原子性
                    temp_path = output_path + ".tmp"
                    with open(temp_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(paragraphs[i:i + chunk_size]))
                    os.rename(temp_path, output_path)

                # 记录成功日志
                with open(log_file, "a", encoding="utf-8") as log:
                    log.write(f"[SUCCESS] {datetime.now():%Y-%m-%d %H:%M:%S} {file} -> {len(paragraphs)} paragraphs\n")

            except Exception as e:
                print(f"处理失败 [{file}]: {str(e)}")
                with open(log_file, "a", encoding="utf-8") as log:
                    log.write(f"[ERROR] {datetime.now():%Y-%m-%d %H:%M:%S} {file} - {str(e)}\n")

def pdf_to_txt(Drama):
    config = load_config()
    settings = config["photo_to_txt"]

    INPUT_FOLDER = f"{config['INPUT_FOLDER']}/{Drama}"
    OUTPUT_FOLDER = f"{config['PROCESS_FOLDER']}/{settings['OUTPUT_FOLDER']}/{Drama}"
    CHUNK_SIZE = int(settings.get("PARAGRAPHS_PER_FILE", 500))

    # 环境检查
    if not os.path.exists(INPUT_FOLDER):
        raise FileNotFoundError(f"输入目录不存在: {INPUT_FOLDER}")

    print(f"📂 输入目录: {os.path.abspath(INPUT_FOLDER)}")
    print(f"📂 输出目录: {os.path.abspath(OUTPUT_FOLDER)}")
    print(f"🔢 分割参数: 每 {CHUNK_SIZE} 段落/文件")
    print(f"🕒 开始时间: {datetime.now():%Y-%m-%d %H:%M:%S}")

    process_folder(INPUT_FOLDER, OUTPUT_FOLDER, CHUNK_SIZE)

    print(f"✅ 处理完成: {datetime.now():%Y-%m-%d %H:%M:%S}")

if __name__ == "__main__":
    try:
        pdf_to_txt("归途七万里")
    except Exception as e:
        print(f"❌ 致命错误: {str(e)}")
        sys.exit(1)
