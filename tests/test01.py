import sys
import os

# 直接用绝对路径替换
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.get_request import APIRequestHandler

# 使用 APIRequestHandler 类 'siliconflow', 'deepseek'
api_handler = APIRequestHandler('models/request.json', 'models/keys.toml', 'siliconflow')

# 加载数据
api_handler.load_data()

# 获取并打印响应文本
response_text = api_handler.get_response_text()
print(response_text)