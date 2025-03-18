import importlib.util
import subprocess

def check_and_install_dependencies():
    try:
        # 读取 requirements.txt 文件
        with open('src/requirements.txt', 'r') as file:
            dependencies = file.read().splitlines()

        for dependency in dependencies:
            # 处理库名和版本号，例如 "requests==2.28.2" 提取出 "requests"
            package_name = dependency.split('==')[0]
            # 检查库是否已经安装
            spec = importlib.util.find_spec(package_name)
            if spec is None:
                print(f"{package_name} 未安装，正在下载...")
                try:
                    # 使用 subprocess 调用 pip 安装库
                    subprocess.check_call(['pip', 'install', dependency])
                    print(f"{package_name} 安装成功。")
                except subprocess.CalledProcessError as e:
                    print(f"安装 {package_name} 时出错: {e}")
            else:
                print(f"{package_name} 已安装。")
    except FileNotFoundError:
        print("未找到 requirements.txt 文件，请检查文件是否存在。")

if __name__ == "__main__":
    check_and_install_dependencies()