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

str = "\n 随着互联网技术的发展，大规模分布式系统在许多领域得到了广泛的应用。这些系统涉及到分布式数据库、微服务架构、云计算平台等，其复杂性和规模都在不断增长。数据一致性和系统的高可用性是设计和运维这些系统时面临的两个最重要的挑战。如何优化大规模分布式系统中的数据一致性和高可用性？"

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