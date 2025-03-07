import os
import concurrent.futures

def run_main_py(file_path):
    """
    运行指定路径下的 main.py 文件
    :param file_path: main.py 文件的完整路径
    """
    try:
        # 构造执行 main.py 文件的命令
        command = f"python {file_path}"
        # 执行命令
        os.system(command)
        print(f"成功执行 {file_path}")
    except Exception as e:
        print(f"执行 {file_path} 时出错: {e}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录
    main_py_files = []

    # 遍历 Text summaries 文件夹
    for root, dirs, files in os.walk(base_dir):
        # 排除 _pycache_ 文件夹
        if "_pycache_" in dirs:
            dirs.remove("_pycache_")
        for file in files:
            if file == "main.py":
                # 构建 main.py 文件的完整路径
                file_path = os.path.join(root, file)
                main_py_files.append(file_path)

    # 使用线程池并行执行 main.py 文件
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_main_py, main_py_files)

if __name__ == "__main__":
    main()