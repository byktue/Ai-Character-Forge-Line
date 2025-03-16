import os
import sys 
from .combination import combination
from concurrent.futures import ThreadPoolExecutor

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 返回上一级目录
parent_dir = os.path.dirname(current_dir)
# 将项目根目录添加到 sys.path 中
sys.path.append(parent_dir)
# 使用绝对导入
from config.config_loader import load_config

# 使用 concurrent.futures.ThreadPoolExecutor 实现线程池

def combination_main(drama):
    # 加载配置
    config = load_config()
    if config is None:
        exit(1)
    parts = set(config["parts"]["parts"]) 
    
    def process_part(part):
        combination(part,drama)

    with ThreadPoolExecutor(max_workers=len(parts)) as executor:
        executor.map(process_part, parts)
        
if __name__ == "__main__":
    combination_main("归途七万里")