from file_processor import traverse_folder
from concurrent.futures import ThreadPoolExecutor
from config_loader import load_config

# 使用 concurrent.futures.ThreadPoolExecutor 实现线程池

def Text_1_main():
    # 加载配置
    config = load_config()
    if config is None:
        exit(1)
    parts = set(config["parts"]["parts"]) 
    
    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=len(parts)) as executor:
        executor.map(traverse_folder, parts)
        
if __name__ == "__main__":
    Text_1_main()