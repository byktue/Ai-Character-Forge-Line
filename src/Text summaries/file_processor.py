import os
from api_request import extract_main_characters, extract_summary  # 添加这行导入语句

def review_and_fix_summary(summary, character_mapping):
    for alias, main_name in character_mapping.items():
        summary = summary.replace(alias, main_name)
    return summary

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

def process_file(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, input_file_path, output_file_path, encoding):
    try:
        with open(input_file_path, 'r', encoding=encoding) as file:
            text = file.read()
        # 提取主要人物及其所有可能的名称
        character_mapping = extract_main_characters(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, text)
        summary = extract_summary(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, text)
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
        print(f"处理文件 {input_file_path} 时出现异常（类型: {type(e).__name__}）: {e}")

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