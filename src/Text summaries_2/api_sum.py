import os
import requests
import time

def api_sum(input_file_path, output_file_path, api_url, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    max_retries = 5  # 最大重试次数
    retry_delay = 10  # 每次重试的延迟时间（秒）

    for attempt in range(max_retries):
        try:
            # 读取输入文件内容
            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            data = {
                "model": "deepseek-ai/DeepSeek-V3",
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            }

            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()

            # 处理响应结果
            result = response.json()
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(str(result))

            print(f"处理并保存文件: {input_file_path} -> {output_file_path}")
            break  # 请求成功，退出重试循环
        except requests.HTTPError as e:
            if e.response.status_code == 429:
                if attempt < max_retries - 1:
                    print(f"请求频率过高，将在 {retry_delay} 秒后重试（第 {attempt + 1} 次重试）...")
                    time.sleep(retry_delay)
                else:
                    print(f"达到最大重试次数，请求失败: {input_file_path}")
            else:
                print(f"请求 API 时出错: {e}")
                break
        except requests.RequestException as e:
            print(f"请求异常: {e}")
            break

    return None
