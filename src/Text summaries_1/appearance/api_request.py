import requests
import time

# 该函数用于从 DeepSeek API 提取文本中主要人物的外貌特征
# 参数：
# DEEPSEEK_API_URL：DeepSeek API 的 URL
# DEEPSEEK_API_KEY：DeepSeek API 的密钥
# DEEPSEEK_MODEL：DeepSeek API 使用的模型名称
# text：需要提取外貌特征的文本
# 返回值：外貌特征列表，如果请求失败则返回空列表
def extract_appearance_features(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, text):
    # 请求头，包含内容类型和授权信息
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    # 请求消息，包含用户指令和文本
    messages = [
        {
            "role": "user",
            "content": f"请提取以下文本中主要人物的外貌特征：{text}"
        }
    ]
    # 请求数据，包含模型名称和消息
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": messages
    }
    # 最大重试次数
    max_retries = 5  
    # 每次重试的延迟时间（秒）
    retry_delay = 5  
    # 进行重试
    for attempt in range(max_retries):
        print(f"正在向 DeepSeek API 发起提取外貌特征请求（第 {attempt + 1} 次尝试）...")
        try:
            # 发送 POST 请求
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
            # 检查响应状态码，如果不是 200 则抛出异常
            response.raise_for_status()
            # 获取响应的 JSON 数据
            result = response.json()
            # 提取外貌特征信息
            features_str = result["choices"][0]["message"]["content"]
            # 按行分割字符串，得到外貌特征列表
            features = features_str.splitlines()
            print("成功从 DeepSeek API 获取到外貌特征信息。")
            return features
        except requests.HTTPError as e:
            print(f"请求 DeepSeek API 时出现 HTTP 错误（类型: {type(e).__name__}）: {e}")
            if e.response.status_code == 429:
                print(f"请求频率过高，将在 {retry_delay} 秒后重试（第 {attempt + 1} 次尝试）...")
                time.sleep(retry_delay)
            else:
                break
        except requests.RequestException as e:
            print(f"请求 DeepSeek API 时出现请求异常（类型: {type(e).__name__}）: {e}")
            break
    print("达到最大重试次数，请求失败。")
    return []