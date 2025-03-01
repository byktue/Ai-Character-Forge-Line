import json
import sys
import os

# 直接用绝对路径替换
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.get_request import APIRequestHandler

# 使用 APIRequestHandler 类 'siliconflow', 'deepseek'
siliconflow_api_handler = APIRequestHandler('models/request.json', 'models/keys.toml', 'siliconflow')
deepseek_api_handler = APIRequestHandler('models/request.json', 'models/keys.toml', 'deepseek')

# 加载数据
siliconflow_api_handler.load_data()
deepseek_api_handler.load_data()

str = "\n 介绍下中国的江油"

# 获取并打印响应文本

response_text = json.loads(deepseek_api_handler.get_response_text(INPUT="将以下问题分成三个步骤：(把结果按步骤，用数组[]的数据形式返回，[]外不允许有输出，[]中的元素为字符串，数组的每个元素需要记录相应步骤的详细信息以传递给下一个节点) \n" + str))
content_array = json.loads(response_text['choices'][0]['message']['content'].strip())
print(content_array, end="\n" + "-" * 50 + "\n")

response_text = json.loads(siliconflow_api_handler.get_response_text(INPUT=content_array[0]) )
OUTPUT1 = response_text['choices'][0]['message']['content']
print(OUTPUT1, end="\n" + "-" * 50 + "\n")

response_text = json.loads(siliconflow_api_handler.get_response_text(INPUT='信息: '+ OUTPUT1 + '接着分析: ' + content_array[1]))
OUTPUT2 = response_text['choices'][0]['message']['content']
print(OUTPUT2, end="\n" + "-" * 50 + "\n")

response_text = json.loads(siliconflow_api_handler.get_response_text(INPUT='信息: '+ OUTPUT2 + '接着分析: ' + content_array[2]))
OUTPUT3 = response_text['choices'][0]['message']['content']
print(OUTPUT3, end="\n" + "-" * 50 + "\n")