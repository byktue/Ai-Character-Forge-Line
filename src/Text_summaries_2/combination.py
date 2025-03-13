import os

def combination(folder_path, output_file):
    # 初始化一个空字符串，用于存储所有文件的内容
    combined_content = ""

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # 以只读模式打开文件，并使用 UTF-8 编码读取内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # 去掉第一行
                    content_lines = lines[1:]
                    content = ''.join(content_lines)
                    # 检查字符数是否少于100，少于则跳过
                    if len(content) < 100:
                        continue
                    # 将当前文件的内容添加到合并内容中，并在后面添加四个换行符作为分割
                    combined_content += content + "\n"
            except Exception as e:
                print(f"处理文件 {file} 时出错: {e}")

    # 如果合并内容不为空，去掉最后多余的四个换行符
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