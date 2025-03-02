# 我的设计理念是像html，每个标签<h1>代表对模型的调用，每个标签里可以有样式来对维度上的信息准确化，最终实现一个递归的程序，不同标签之间可以用src连接其他标签。
# 以下HtmlParser应该是对整个html文档树进行构建出真正的model分析调用树
# 正则表达式匹配标签：<tag>content</tag>
import re
from collections import deque

class Node:
    def __init__(self, tag, attrs=None, children=None, text=""):
        self.tag = tag  # 标签名
        self.attrs = attrs if attrs else {}  # 属性字典
        self.children = children if children else []  # 子节点列表
        self.text = text  # 文本内容
        self.cache = []

    def __repr__(self):
        return f"Node(tag={self.tag}, attrs={self.attrs}, text={self.text}, children={len(self.children)})"
    
    def pretty_print(self, level=0):
        """递归打印Node结构"""
        indent = "  " * level
        attr_str = " ".join(f'{k}="{v}"' for k, v in self.attrs.items())
        attr_str = f" {attr_str}" if attr_str else ""
        print(f"{indent}<{self.tag}{attr_str}>\n{indent}  {self.text.strip()}")
        for child in self.children:
            child.pretty_print(level + 1)
        print(f"{indent}</{self.tag}>")


class HtmlParser:
    def __init__(self, html):
        self.html = self.remove_comments(html.strip())
        self.root = self.parse()

    def remove_comments(self, html):
        return re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

    def parse(self):
        """解析HTML并构建DOM树"""
        tokens = self.tokenize(self.html)
        return self.build_tree(tokens)

    def tokenize(self, html):
        """将HTML转换为标签、文本等token"""
        pattern = re.compile(r"(</?[\w\d]+[^>]*>)|([^<>]+)")
        return [match.group(0).strip() for match in pattern.finditer(html) if match.group(0).strip()]

    def build_tree(self, tokens):
        """从tokens构建DOM树"""
        stack = deque()
        root = Node("root")
        current = root

        for token in tokens:
            if token.startswith("</"):  # 结束标签
                if stack:
                    current = stack.pop()
            elif token.startswith("<"):  # 起始标签
                tag, attrs = self.parse_tag(token)
                node = Node(tag, attrs)
                current.children.append(node)
                stack.append(current)
                current = node
            else:  # 纯文本
                current.text += token

        return root

    def parse_tag(self, tag_str):
        """解析HTML标签及其属性"""
        tag_parts = tag_str[1:-1].split()
        tag_name = tag_parts[0]
        attrs = {}

        for part in tag_parts[1:]:
            if '=' in part:
                key, value = part.split("=", 1)
                attrs[key] = value.strip('"')

        return tag_name, attrs


