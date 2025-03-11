import os

def check_non_empty_file_exists(file_path):
    """
    检测指定路径的文件是否存在且非空
    :param file_path: 文件的完整路径
    :return: 如果文件存在且非空返回 True，否则返回 False
    """
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return True
    return False