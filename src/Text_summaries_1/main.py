from file_processor import traverse_folder
from concurrent.futures import ThreadPoolExecutor

# 使用 concurrent.futures.ThreadPoolExecutor 实现线程池

def Text_1_main():
    parts = {
        "appearance",
        "events",
        "identity",
        "name",
        "personality",
        "utterance"
    }
    
    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=len(parts)) as executor:
        executor.map(traverse_folder, parts)
        
if __name__ == "__main__":
    Text_1_main()