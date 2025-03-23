# 启发式深度优先遍历
# 有向图里有环。存在两个节点之间有正反两条边的情况。


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from tqdm import tqdm
import csv

from smallest_tree import Label2Weight, GetGraph, DFS, Is_connected_dfs, Prim, Min_mst2seq

def GetInfo(file_path):
    #print("开始获取图信息~")
    
    try:
        graph = nx.nx_agraph.read_dot(file_path)
        # 检查图是否为空
        #if graph.number_of_nodes() > 0:
            #print("图提取成功，包含节点：", graph.number_of_nodes())
        #else:
            #print("图提取成功，但图为空。")
    except Exception as e:
        #print("提取图失败：", e)
        return -1

    # 获取节点和边的信息
    nodes = list(graph.nodes(data=True))
    int_nodes = [int(item) for item, _ in nodes]
    nodes_labels = {int(node): dict_item['label'] for node, dict_item in nodes}

    edges = list(graph.edges(data=True))
    int_edges_labels = [(int(item1), int(item2), str(label_item['label'])) for item1, item2, label_item in edges]

    # 输出节点和边的信息
    #print("Nodes:", int_nodes, '    节点数:', len(int_nodes), '\n')
    #print("Nodes Labels:", nodes_labels,  '    节点标签数:', len(int_nodes), '\n')
    #print("Edges:", int_edges_labels,   '    边数:', len(int_edges_labels), '\n')

    # map
    node_mapping = {node: i for i, node in enumerate(int_nodes)}
    edge_mapping = {edge: i for i, edge in enumerate(int_edges_labels)}
    #print("Edge Map:", edge_mapping,   '    map长度:', len(edge_mapping), '\n')
    #print("成功获取图信息！")
    return nodes, int_nodes, nodes_labels, edges, int_edges_labels, node_mapping, edge_mapping


def EdgeCheck(e, int_edges_labels, edge_mapping):
    # 传进来的e中的边数只能是＞=1
    if len(e) == 1:
        if 'DDG' in int_edges_labels[edge_mapping[e[0]]][2]:  # 一条边的情况直接使用，并判断是控制依赖还是数据依赖
            return 'd', e[0]
        else:
            return 'c', e[0]
    else:
        ddg_edges = []
        cdg_edges = []
        for e_item in e:
            if 'DDG' in int_edges_labels[edge_mapping[e_item]][2]:
                ddg_edges.append(e_item)
            else:
                cdg_edges.append(e_item)
        if cdg_edges:
            cur_point = cdg_edges[0][0]
            min_point = cdg_edges[0][1]
            label = cdg_edges[0][2]
            for cdg_edge in cdg_edges:
                if cdg_edge[1] < min_point:  # 优先选控制依赖边，且多条控制依赖边选目标节点最小的
                    min_point = cdg_edge[1]
                    label = cdg_edge[2]
                else:
                    continue
            return 'c', (cur_point, min_point, label)
        else:
            cur_point = ddg_edges[0][0]
            min_point = ddg_edges[0][1]
            label = ddg_edges[0][2]
            for ddg_edge in ddg_edges:
                if ddg_edge[1] < min_point:  # 后选数据依赖边，且数据依赖边优先选目标节点最小的
                    min_point = ddg_edge[1]
                    label = ddg_edge[2]
                else:
                    continue
            return 'd', (cur_point, min_point, label)
        

def SequenceExpand(edge_type, e, result, int_edges_clone, nodes_labels):
    if edge_type == 'c':  # 控制依赖压入目标节点
        result.append(nodes_labels[e[1]])
        int_edges_clone.remove(e)
        
    elif edge_type == 'd':  # 数据依赖压入边属性和目标节点
        result.append(e[2])
        result.append(nodes_labels[e[1]])
        int_edges_clone.remove(e)
        

def DFSRule(int_nodes, nodes_labels, int_edges_labels, edge_mapping):
    result = []
    int_edges_clone = []
    useful_father_stack = []
    # 节点、转换成整型的节点、节点的标签、边、转换成整型和字符串的边、节点map、边map
    
    int_edges_clone = int_edges_labels[:]

    start_node = int_nodes[0]  # 初始节点是第一个节点
    result.append(nodes_labels[start_node])
    useful_father_stack.append(start_node)

    i = 0
    while len(int_edges_clone):  # 还有边没被遍历时
        backtracking_edges = []
        forward_edges = []
        
        for edge in int_edges_clone:
            if edge[0] == start_node:  # 找到所有以该节点作为起始节点的边
                if edge[1] in result:  # 判断回溯边还是前向边
                    backtracking_edges.append(edge)
                else:
                    forward_edges.append(edge)
            else:
                continue

        if len(backtracking_edges):  # 回溯边处理
            edge_type, backtracking_edge = EdgeCheck(backtracking_edges, int_edges_labels, edge_mapping)
            SequenceExpand(edge_type, backtracking_edge, result, int_edges_clone, nodes_labels)

        elif len(forward_edges):  # 前向边处理
            edge_type, forward_edge = EdgeCheck(forward_edges, int_edges_labels, edge_mapping)
            SequenceExpand(edge_type, forward_edge, result, int_edges_clone, nodes_labels)
            useful_father_stack.append(forward_edge[1])
            start_node = useful_father_stack[-1]

        else:  # 该节点无边时
            useful_father_stack.pop()
            if len(useful_father_stack):
                start_node = useful_father_stack[-1]
            elif not len(useful_father_stack) and len(int_edges_clone):
                start_node = int_edges_clone[0][0]
                result.append(nodes_labels[start_node])
                useful_father_stack.append(start_node)
            else:
                print("边已遍历完！")

        i = i + 1
        #print("次数：", i)
    
    # print(result,   '    长度:', len(result), '\n')

    return result


if __name__ == '__main__':
    # 文件夹路径

    folder_path = {"novul": '/mnt/sda/.../Devign/novuldotsingle',  # 添加无缺陷pdg绝对路径
                   "vul": '/mnt/sda/.../Devign/vuldotsingle',  # 添加缺陷pdg绝对路径
                   }

    save_path = {"novul_seq_save_path": '/mnt/sda/.../Devign/novulpdfseq',  # 添加无缺陷pdgseq保存路径
            "vul_seq_save_path": '/mnt/sda/.../Devign/vulpdfseq',  # 添加缺陷pdgseq保存路径
            }
    
    for value in save_path.values():
        if not os.path.exists(value):
            os.makedirs(value)


    dfs_seq = []  # 保存所有文件的序列

    files_path = []
    invalifile = 0

    folder = "vul"  # 修改，现在处理的是有缺陷还是无缺陷的图

    for filename in os.listdir(folder_path[folder]):
        # 拼接文件的完整路径
        files_path.append(os.path.join(folder_path[folder], filename))
    print("文件总数：", len(files_path))


    i = 0  # 由于内存限制，无法一下处理大量文件，变成每次处理400个pdg。
    end = min(i+400, len(files_path))

    for j in tqdm(range(i, end)):
    #for j in tqdm(range(0, len(files_path))):
        file_path = files_path[j]
        filename = file_path.split("\\")[-1]
        num = re.search(r'-(\d+)-', filename)
        if num:
            # 如果找到匹配项，提取数字
            number = num.group(1)
            print(number)
        else:
            #print("没有找到两个短横线之间的数字")
            continue

        #print("file_list:", len(file_list))

        info = GetInfo(file_path)
        if info == -1:
            continue
        else:
            nodes, int_nodes, nodes_labels, edges, int_edges_labels, node_mapping, edge_mapping = info[0], info[1], info[2], info[3], info[4], info[5], info[6]
        if len(nodes) and len(edges):  # 如果有节点且有边
            res1 = DFSRule(int_nodes, nodes_labels, int_edges_labels, edge_mapping)
            #print("PDG序列完成！")

        
        elif len(nodes) and not len(edges):
            print("有节点无边！" + str(number))
            invalifile += 1
            continue

        elif not len(nodes) and len(edges):
            print("有边无节点！" + str(number))
            invalifile += 1
            continue

        else:
            print("无节点无边！" + str(number))
            invalifile += 1
            continue
        
        if folder == "novul":
            with open(save_path["novul_seq_save_path"] + f"{folder}" + "_graph2seq_"+ str(i) + ".csv", 'a') as file:
                writer = csv.writer(file)
                code_string = ','.join(map(str, res1))
                writer.writerow([number, res1])

        elif folder == "vul":
            with open(save_path["vul_seq_save_path"] + f"{folder}" + "_graph2seq_"+ str(i) + ".csv", "a") as file:
                writer = csv.writer(file)
                code_string = ','.join(map(str, res1))
                writer.writerow([number, res1])


    print("无效文件：", invalifile, '\n')
                

