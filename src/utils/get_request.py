import json
import requests
import toml

class APIRequestHandler:
    def __init__(self, json_file, toml_file, id):
        self.json_file = json_file
        self.toml_file = toml_file
        self.id = id
        self.data = None
        self.keys = None
        self.url = None
        self.payload = None
        self.headers = None
        

    def load_data(self):
        # 读取 JSON 文件
        with open(self.json_file, 'r', encoding='utf-8') as json_file:
            self.data = json.load(json_file)

        # 读取 TOML 文件
        with open(self.toml_file, 'r', encoding='utf-8') as toml_file:
            self.keys = toml.load(toml_file)

        # 从 JSON 数据中获取 URL、payload 和 headers
        data_item = next((item for item in self.data if item['id'] == self.id), None)

        if data_item is not None:
            # 如果找到了匹配的字典
            self.url = data_item['url']
            self.payload = data_item['payload']
            self.headers = data_item['headers']

            # 查找 keys 中 api_providers 列表中 id 匹配的字典，并获取 apikey
            api_provider = next((provider for provider in self.keys['api_providers'] if provider['id'] == self.id), None)
            if api_provider is not None:
                self.headers['Authorization'] = self.headers['Authorization'] + api_provider['apikey']
            else:
                print(f"未找到 api_providers 中 id 为 {self.id} 的提供者")
        else:
            print(f"未找到 id 为 {self.id} 的数据项")

    def send_request(self, INPUT):
        # 发送 POST 请求
        if INPUT:
            for message in self.payload["messages"]:
                if message["role"] == "user":
                    message["content"] = INPUT
            
        response = requests.request("POST", self.url, json=self.payload, headers=self.headers)
        return response

    def get_response_text(self, INPUT = None):
        # 返回响应的文本
        response = self.send_request(INPUT)
        return response.text
