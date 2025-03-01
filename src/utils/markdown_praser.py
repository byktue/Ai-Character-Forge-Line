import re

class Node:
    def __init__(self, tag, content=None):
        self.tag = tag  # 节点的标签（如标题、段落等）
        self.content = content  # 节点的内容（文本或子节点）
        self.children = []  # 存储子节点（对于列表、段落等元素）

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self, level=0):
        indent = ' ' * (level * 2)
        if not self.children:
            return f"{indent}<{self.tag}>: {self.content}"
        else:
            children_str = "\n".join(child.__repr__(level + 1) for child in self.children)
            return f"{indent}<{self.tag}>\n{children_str}\n{indent}</{self.tag}>"

class MarkdownParser:
    def __init__(self):
        self.root = Node('root')
    
    def parse(self, markdown_text):
        lines = markdown_text.split('\n')
        current_node = self.root
        unordered_list_node = None  # 用于存储当前的无序列表节点

        for line in lines:
            # 处理标题
            if line.startswith('#'):
                level = line.count('#')  # 标题等级
                content = line.lstrip('#').strip()
                header_node = Node(f'h{level}', content)
                current_node.add_child(header_node)
            # 处理有序列表项（数字.开头的）
            elif re.match(r'^\d+\.', line):
                # 如果当前没有无序列表节点，创建一个
                if unordered_list_node is None:
                    unordered_list_node = Node('ul')
                    current_node.add_child(unordered_list_node)
                
                list_item_content = line.split('.', 1)[1].strip()  # 获取列表项的内容
                item_node = Node('li', list_item_content)
                unordered_list_node.add_child(item_node)
            # 处理非数字开头的行，退出无序列表
            elif not line.startswith(' ') and not line.startswith('#') and not re.match(r'^\d+\.', line):
                # 如果是空行或段落，退出当前无序列表（如果有）
                if unordered_list_node is not None:
                    unordered_list_node = None

                # 处理普通段落
                paragraph_node = Node('p', line.strip())
                current_node.add_child(paragraph_node)

            elif line.strip():  # 非空行，处理段落
                paragraph_node = Node('p', line.strip())
                current_node.add_child(paragraph_node)
            else:
                continue  # 空行跳过
    
    def get_parsed_tree(self):
        return self.root
    
    def print_tree(self):
        print(self.root.__repr__())