import requests
import json

# 硅基流动 API 信息
api_url = "https://api.siliconflow.cn/v1/chat/completions"  # 根据实际情况修改
api_key = "your_api_key_here"  # 替换为你的 API 密钥

# 请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 请求体
data = {
    "model": "deepseek-ai/DeepSeek-V3",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你的具体问题"}
    ],
    "stream": False,
    "max_tokens": 512,
    "stop": None,
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "response_format": {
        "type": "text"
    }
}

# 发送请求
response = requests.post(api_url, headers=headers, data=json.dumps(data))

# 处理响应
if response.status_code == 200:
    result = response.json()
    print(result['choices'][0]['message']['content'])
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(response.text)