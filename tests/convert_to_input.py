import json

# 打开文件并读取内容
with open('data/avatar.md', 'r', encoding='utf-8') as file:
    file_content = file.read()

# 替换换行符\n为一个空格（你可以根据需求替换为其他符号）
file_content = file_content.replace('\n', ' ')
file_content = file_content.replace('\\', '\\\\')
file_content = file_content.replace('"', '\\"')

# 打印处理后的内容
print(file_content)