import re
import os
from tqdm import tqdm

def remove_comments_from_file(file_path):
    # 定义单行和多行注释的正则表达式
    single_line_comment_pattern = r'//.*?$'
    multi_line_comment_pattern = r'/\*.*?\*/'
    
    # 读取文件内容
    with open(file_path, 'r') as file:
        content = file.read()
    
    # 删除单行注释
    content = re.sub(single_line_comment_pattern, '', content, flags=re.MULTILINE)
    
    # 删除多行注释
    content = re.sub(multi_line_comment_pattern, '', content, flags=re.DOTALL)
    
    # 写回文件
    with open(file_path, 'w') as file:
        file.write(content)

def remove_comments_from_directory(directory_path):
    # 遍历目录中的所有文件
    for root, dirs, files in tqdm(os.walk(directory_path), desc='去除注释'):
        for file in files:
            if file.endswith('.c'):
                file_path = os.path.join(root, file)
                #print(f'Removing comments from: {file_path}')
                remove_comments_from_file(file_path)

# 替换为你的目录路径
directory_path = '/mnt/sda/zhangky23/pythoncode/Devign-dataset/ffmpegqemu/v6-norepeat/vul'
remove_comments_from_directory(directory_path)