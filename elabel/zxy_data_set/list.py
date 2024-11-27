import os
import sys

def list_files_absolute(directory):
    """
    列出指定目录下的所有文件的绝对路径。
    :param directory: 目标目录路径
    """
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在。")
        return

    print(f"目录 '{directory}' 下的所有文件（绝对路径）：")
    for root, _, files in os.walk(directory):
        for file in files:
            # 输出文件的绝对路径
            print(os.path.abspath(os.path.join(root, file)))


if __name__ == "__main__":
    # 检查是否提供了目标目录
    if len(sys.argv) < 2:
        print("用法: python list_files_absolute.py <目录路径>")
        sys.exit(1)

    # 读取目标目录路径
    target_dir = sys.argv[1]
    list_files_absolute(target_dir)