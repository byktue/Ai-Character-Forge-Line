import json
import sys
import os
import markdown

# 直接用绝对路径替换
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.html_praser import HtmlParser

# 打开文件并读取内容
with open('data/avatar.md', 'r', encoding='utf-8') as file:
    file_content = file.read()

# # 替换换行符\n为一个空格（你可以根据需求替换为其他符号）
# file_content = file_content.replace('\n', ' ')
# file_content = file_content.replace('\\', '\\\\')
# file_content = file_content.replace('"', '\\"')

html = markdown.markdown(file_content)
parser = HtmlParser()
root_node = parser.parse(html)

def print_tree(nodes, indent=0):
    if isinstance(nodes, list):  # 如果是节点列表，逐个打印
        for node in nodes:
            print_tree(node, indent)
    else:  # 如果是单个节点
        print("  " * indent + f"<{nodes.tag}>")
        if (nodes.content != ''):
            print("  " * indent + nodes.content)
        for child in nodes.children:
            print_tree(child, indent + 1)
        print("  " * indent + f"</{nodes.tag}>")

# 假设 root_node 是解析后的节点
print_tree(root_node)