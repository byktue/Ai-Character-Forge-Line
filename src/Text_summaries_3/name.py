import os
import requests

def name_sum(file_path, output_file_path, API_URL, API_KEY, MODEL , AVATAR):
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
            "model": MODEL,
            "messages": [
                {"role": "system", "content": f"请提取文本中 {AVATAR} 的名称及别名，如果有名称转变，请标注出转变的大概的事件描述"},
                {"role": "user", "content": content}
            ]
        }
        # 发送请求
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # 提取信息
        events_info = result['choices'][0]['message']['content']

        # 检查输出文件所在的目录是否存在，如果不存在则创建
        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 将提取的事件信息写入文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(events_info)
        print(f"提取信息已存储到 {output_file_path}")
        return events_info
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return None