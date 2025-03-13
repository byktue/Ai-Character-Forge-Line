import os
from api_request import extract_character_traits

def format_traits(traits):
    output = "对于文本中主要人物的性格特点：\n"
    output += f"  性格特点：{', '.join(traits)}\n"
    return output

def process_file(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, input_file_path, output_file_path, encoding):
    try:
        with open(input_file_path, 'r', encoding=encoding) as file:
            text = file.read()
        traits = extract_character_traits(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, text)
        if traits:
            # 只有在提取到性格特点信息时，才创建输出文件
            formatted_traits = format_traits(traits)
            with open(output_file_path, 'w', encoding=encoding) as output_file:
                output_file.write(formatted_traits)
            print(f"已处理并保存文件: {input_file_path} -> {output_file_path}")
        else:
            print(f"未提取到有效性格特点信息，跳过文件: {input_file_path}")
    except Exception as e:
        print(f"处理文件 {input_file_path} 时出现异常（类型: {type(e).__name__}）: {e}")

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