import os
import requests

def api_sum(file_path, output_file_path, API_URL, API_KEY):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # 构建请求体
        data = {
            "model": "deepseek-chat-7b",
            "messages": [
                {"role": "system", "content": "请从提供的文本中提取事件信息。"},
                {"role": "user", "content": content}
            ]
        }
        # 发送请求
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # 提取事件信息
        events_info = result['choices'][0]['message']['content']

        # 将提取的事件信息写入文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(events_info)
        print(f"提取的事件信息已存储到 {output_file_path}")
        return events_info
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return None
