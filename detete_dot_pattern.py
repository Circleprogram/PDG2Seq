import os
import re
from tqdm import tqdm
# import networkx as nx


def write_to_file(content, file_path):
    with open(file_path, 'a') as file:
        file.write(content + '\n')


html_entity_map = {
    '&lt;': '<',
    '&gt;': '>',
    '&amp;': '&',
    '&quot;': "'",
    '&apos;': "'"
}


def replace_html_entities(text, entity_map):
    pattern = re.compile('|'.join(map(re.escape, entity_map.keys())))
    return pattern.sub(lambda m: entity_map[m.group()], text)


def compress_outermost_brackets_to_single_line(text):
    pattern = re.compile(r'<([^<>]*(?:<(?:[^<>]+)?>[^<>]*)*)>', re.DOTALL)

    def replace_func(match):
        inner_text = match.group(1).replace('\n', ' ').strip()
        return f'<{inner_text}>'

    return pattern.sub(replace_func, text)


# def process_dot_file(file_path, output_file_path):
# zyj:我不打算在这里处理图，只打算得到dot图文件，所以这里把后面networkx的部注释掉了，于是也把函数传入参数改了改
def process_dot_file(file_path):
    with open(file_path, 'r', errors='ignore') as file:
        content = file.read()
    content = compress_outermost_brackets_to_single_line(content)
    with open(file_path, 'w') as file:
        file.write(content)
    with open(file_path, 'r', errors='ignore') as file:
        lines = file.readlines()

    processed_lines = []
    for line in lines:
        line = re.sub(r'(<)([^<>]*(?:<(?:[^<>]+)?>[^<>]*)*)(>)', r'"\2"', line)
        #line = re.sub(r'<SUB>|</SUB>', '', line)
        #line = re.sub(r'<SUB>\d+</SUB>','',line)
        #line = re.sub(r'\([^,]*,', '(', line)
        line = replace_html_entities(line, html_entity_map)
        processed_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)

    # G = nx.drawing.nx_pydot.read_dot(file_path)
    # nodes_info = "Nodes in the graph:\n" + '\n'.join(str(node) for node in G.nodes(data=True))
    # edges_info = "\nEdges in the graph: " + str(G.edges())
    # write_to_file(nodes_info, output_file_path)
    # write_to_file(edges_info, output_file_path)

"""
# 他这一段是根据他的文件结构编写的，我直接重写就行
def process_all_dot_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            print(f'root is {root}')
            print(f'file_name is {file_name}')
            if file_name.endswith('.dot'):
                file_path = os.path.join(root, file_name)
                print(file_path)
                folder_name = os.path.basename(root)
                output_file_name = f"{folder_name}.txt"
                print(output_file_name)
                output_file_path = os.path.join(root, output_file_name)
                # process_dot_file(file_path, output_file_path)
                print(f"文件 {file_name} 处理完成，结果已保存至 {output_file_path}")
            break
        break
"""
def process_all_dot_files(folder_path):
    for filename in tqdm(os.listdir(folder_path), desc = folder_path):
        # print(filename)
        process_dot_file(os.path.join(folder_path, filename))


# Example usage
# folder_path = '/Users/zzz/Downloads/2023.9.5整理/Dataset-sard'
folder_path = r'/mnt/sda/zhangky23/pythoncode/Devign-dataset/ffmpegqemu/v4-norepeat/codecpg-novuldotsingle-clean'
process_all_dot_files(folder_path)
