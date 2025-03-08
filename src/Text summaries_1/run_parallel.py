import os
import subprocess
import concurrent.futures
import time

def run_main_py(file_path):
    """
    运行指定路径下的 main.py 文件
    :param file_path: main.py 文件的完整路径
    """
    try:
        # 使用 subprocess.run 来执行命令
        result = subprocess.run(['python', file_path], check=True)
        if result.returncode == 0:
            print(f"成功执行 {file_path}")
        else:
            print(f"执行 {file_path} 时出错，返回码: {result.returncode}")
    except Exception as e:
        print(f"执行 {file_path} 时出错: {e}")

def main():
    start_time = time.time()  # 记录开始时间
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
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(run_main_py, main_py_files)
    except KeyboardInterrupt:
        print("程序被中断")
    finally:
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算运行时间
        print(f"程序运行时间: {elapsed_time:.2f} 秒")

if __name__ == "__main__":
    main()