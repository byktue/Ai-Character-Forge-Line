import requests
import time

def extract_main_characters(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    messages = [
        {
            "role": "user",
            "content": f"请提取以下文本中每个人物的所有可能名称，以人物为单位列出，格式为人物标准名称:别名1,别名2,... 。示例：张三:小张,三哥 。文本：{text}"
        }
    ]
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": messages
    }
    max_retries = 5  # 最大重试次数
    retry_delay = 5  # 每次重试的延迟时间（秒）
    for attempt in range(max_retries):
        print(f"正在向 DeepSeek API 发起提取主要人物名称请求（第 {attempt + 1} 次尝试）...")
        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            characters_str = result["choices"][0]["message"]["content"]
            character_mapping = {}
            for line in characters_str.splitlines():
                if ':' in line:
                    main_name, aliases = line.split(':')
                    all_names = [main_name] + aliases.split(',')
                    for name in all_names:
                        character_mapping[name] = main_name
            print("成功从 DeepSeek API 获取到主要人物名称映射。")
            return character_mapping
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
    return {}

def extract_summary(DEEPSEEK_API_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    messages = [
        {
            "role": "user",
            "content": f"请总结以下文本中的主要人物、人物性格、外貌形象、发生的事件、出现的人物话语、口头禅：{text}"
        }
    ]
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": messages
    }
    max_retries = 5  # 最大重试次数
    retry_delay = 5  # 每次重试的延迟时间（秒）
    for attempt in range(max_retries):
        print(f"正在向 DeepSeek API 发起请求（第 {attempt + 1} 次尝试）...")
        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            summary = result["choices"][0]["message"]["content"]
            print("成功从 DeepSeek API 获取到响应。")
            return summary
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
    return None