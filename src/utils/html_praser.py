import re

# 我的设计理念是像html，每个标签<h1>代表对模型的调用，每个标签里可以有样式来对维度上的信息准确化，最终实现一个递归的程序，不同标签之间可以用src连接其他标签。
# 以下HtmlParser应该是对整个html文档树进行构建出真正的model分析调用树
# 正则表达式匹配标签：<tag>content</tag>
class HtmlParser:
    def __init__(self):
        self.tag_re = re.compile(r'<(\/?)(\w+)(.*?)>(.*?)</\2>', re.DOTALL)
    
    def parse(self, html):
        # 解析 HTML
        self.html = html
        return self._parse_nodes(self.html)
    
    def _parse_nodes(self, html):
        nodes = []
        while html:
            match = self.tag_re.search(html)
            if not match:
                break
            tag = match.group(2)
            is_closing_tag = match.group(1) == "/"
            content = match.group(4)
            # 跳过当前标签和内容
            html = html[match.end():]
            if not is_closing_tag:
                node = Node(tag, content)
                nodes.append(node)
                # 递归解析子节点
                node.children = self._parse_nodes(content)
        return nodes

class Node:
    def __init__(self, tag, content):
        self.tag = tag
        self.content = self.extract_content_before_tag(content)
        self.children = []

    def __repr__(self):
        return f"<{self.tag}>{self.content}</{self.tag}>"
    
    def extract_content_before_tag(self, content):
        # 正则表达式：匹配第一个由 <> 包裹的标签前的内容
        match = re.match(r"^(.*?)(?=<\w)", content.strip())  # 匹配到第一个 '<标签>' 前的内容
        if match:
            return match.group(1).strip()  # 返回标签前的文本，去除两边的空白字符
        return content.strip()  # 如果没有找到标签，则返回原始内容