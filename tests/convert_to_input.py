import json
import sys
import os
import markdown

# 直接用绝对路径替换
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.markdown_praser import MarkdownParser

# 打开文件并读取内容
with open('data/avatar.md', 'r', encoding='utf-8') as file:
    file_content = file.read()

# # 替换换行符\n为一个空格（你可以根据需求替换为其他符号）
# file_content = file_content.replace('\n', ' ')
# file_content = file_content.replace('\\', '\\\\')
# file_content = file_content.replace('"', '\\"')

# # 打印处理后的内容
# parser = MarkdownParser()
# parser.parse(file_content)

# # 输出树形结构
# parsed_tree = parser.get_parsed_tree()
# parser.print_tree()

html = markdown.markdown(file_content)
print(html)
