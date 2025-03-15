from config_loader import load_config
from combination import combination
from concurrent.futures import ThreadPoolExecutor

# 使用 concurrent.futures.ThreadPoolExecutor 实现线程池

def combination_main():
    # 加载配置
    config = load_config()
    if config is None:
        exit(1)
    parts = set(config["parts"]["parts"]) 

    with ThreadPoolExecutor(max_workers=len(parts)) as executor:
        executor.map(combination, parts)
        
if __name__ == "__main__":
    combination_main()