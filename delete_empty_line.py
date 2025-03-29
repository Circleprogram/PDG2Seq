import re
import os
from tqdm import tqdm
def remove_empty_lines_from_file(file_path):
    # 读取文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 移除空行
    non_empty_lines = [line for line in lines if line.strip()]

    # 写回文件
    with open(file_path, 'w') as file:
        file.writelines(non_empty_lines)

def remove_empty_lines_from_directory(directory_path):
    # 遍历目录中的所有文件
    for root, dirs, files in tqdm(os.walk(directory_path), desc='去除空行'):
        for file in files:
            if file.endswith('.c'):
                file_path = os.path.join(root, file)
                print(f'Removing empty lines from: {file_path}')
                remove_empty_lines_from_file(file_path)

# 替换为你的目录路径
directory_path = '/mnt/sda/zhangky23/pythoncode/Devign-dataset/ffmpegqemu/v6-norepeat/novul'
remove_empty_lines_from_directory(directory_path)