import json
import re
from utils.get_request import APIRequestHandler

class RootNode():
    def __init__(self, root):
        self.root = root
        self.id_map = self.build_id_map()

    def build_id_map(self):
        """遍历所有节点，收集具有相同 id 的节点"""
        id_map = {}
        self._traverse_with_id(self.root, id_map)
        return id_map

    def _traverse_with_id(self, node, id_map):
        """递归遍历节点树，收集 id"""
        if not node:
            return

        # 如果节点有 id，加入 id_map
        if "id" in node.attrs:
            node_id = node.attrs["id"]
            if node_id not in id_map:
                id_map[node_id] = []
            id_map[node_id].append(node)

        # 递归遍历子节点
        for child in node.children:
            self._traverse_with_id(child, id_map)

    def pretty_print_id_map(self):
        """打印 id_map 结构"""
        for node_id, nodes in self.id_map.items():
            print(f'ID="{node_id}" 对应 {len(nodes)} 个节点:')
            for node in nodes:
                print(f'  <{node.tag}> {node.text.strip()}')
    
    def run_a_node(self, node, text = None):
        matches = []
        if node and hasattr(node, "text"):
            pattern = r"\{\{(.*?)\}\}"
            matches = re.findall(pattern, node.text)
            # if len(matches) > 0:
            #     for match in matches:
            #         print(self.id_map[match])
        if node and hasattr(node, "children"):
            for child in node.children:
                self.run_a_node(child)

        if node.tag == "div":
            deepseek_api_handler = APIRequestHandler('models/request.json', 'models/keys.toml', 'deepseek')
            deepseek_api_handler.load_data()
            if "id" in node.attrs:
                node_id = node.attrs["id"]
            if text is not None:
                response_text = json.loads(deepseek_api_handler.get_response_text(INPUT=text + "\n" + node.text))
                node.cache.append({node_id : response_text['choices'][0]['message']['content']})
            pass
        elif node.tag == "p":
            pass
        elif node.tag == "ol":
            pass
        elif node.tag == "li":
            pass
        elif node.tag == "ul":
            pass
        elif node.tag == "h1":
            pass
        elif node.tag == "h2":
            deepseek_api_handler = APIRequestHandler('models/request.json', 'models/keys.toml', 'deepseek')
            deepseek_api_handler.load_data()
            if len(matches) > 0:
                for match in matches:
                    for quote_node in self.id_map[match]:
                        self.run_a_node(quote_node, node.text)
            hint = ""
            for child in node.children:
                hint = "\n ".join(f"{k}:{v}" for item in child.cache for k, v in item.items())
            if hasattr(node, "text") and node.text != "":
                response_text = json.loads(deepseek_api_handler.get_response_text(INPUT=node.text + hint))
                node.cache.append({"复述": response_text['choices'][0]['message']['content']})
        elif node.tag == "h3":
            pass
        elif node.tag == "h4":
            pass
        elif node.tag == "root":
            deepseek_api_handler = APIRequestHandler('models/request.json', 'models/keys.toml', 'deepseek')
            deepseek_api_handler.load_data()
            hint = ""
            for child in node.children:
                hint = "\n ".join(f"{k}:{v}" for item in child.cache for k, v in item.items())
            response_text = json.loads(deepseek_api_handler.get_response_text(INPUT=node.text + hint))
            print(response_text['choices'][0]['message']['content'])
        else:
            raise ValueError(f"Unkown tag: {node.tag}")