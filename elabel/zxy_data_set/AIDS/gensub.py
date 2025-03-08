# import networkx as nx
# import random

# def read_graph_from_file(file_path):
#     """
#     从文件中读取图数据并构建图
#     """
#     G = nx.Graph()
#     with open(file_path, 'r') as file:
#         for line in file:
#             parts = line.strip().split()
#             if not parts:
#                 continue
#             if parts[0] == 't':
#                 # 图的总信息，可以忽略或记录
#                 vertex_number = int(parts[1])
#                 edge_number = int(parts[2])
#             elif parts[0] == 'v':
#                 # 添加节点
#                 vertex_id = int(parts[1])
#                 vertex_label = parts[2]
#                 vertex_degree = int(parts[3])
#                 G.add_node(vertex_id, label=vertex_label, degree=vertex_degree)
#             elif parts[0] == 'e':
#                 # 添加边
#                 source = int(parts[1])
#                 target = int(parts[2])
#                 G.add_edge(source, target)
#     return G

# def find_connected_nodes(G, k):
#     """
#     从图中找到一个包含 k 个节点的连通子图
#     """
#     if k > len(G.nodes):
#         raise ValueError("k 不能大于图的节点数")
    
#     # 随机选择一个起始节点
#     start_node = random.choice(list(G.nodes))
    
#     # 使用 BFS 扩展连通节点
#     visited = set()
#     queue = [start_node]
    
#     while queue and len(visited) < k:
#         node = queue.pop(0)
#         if node not in visited:
#             visited.add(node)
#             # 将邻居节点加入队列
#             for neighbor in G.neighbors(node):
#                 if neighbor not in visited:
#                     queue.append(neighbor)
    
#     # 如果找到的节点数不足 k，重新选择起始节点并重试
#     if len(visited) < k:
#         return find_connected_nodes(G, k)
    
#     return list(visited)

# def generate_connected_induced_subgraph(G, k):
#     """
#     生成包含 k 个节点的连通诱导子图
#     """
#     connected_nodes = find_connected_nodes(G, k)
#     induced_subgraph = G.subgraph(connected_nodes)
#     return induced_subgraph

# def renumber_subgraph(subgraph):
#     """
#     对子图的节点重新编号，从 0 开始
#     """
#     # 创建节点映射字典
#     node_mapping = {old_node: new_node for new_node, old_node in enumerate(subgraph.nodes)}
    
#     # 重新编号节点
#     renumbered_subgraph = nx.relabel_nodes(subgraph, node_mapping)
    
#     return renumbered_subgraph

# def write_subgraph_to_file(subgraph, output_file):
#     """
#     将诱导子图按照输入格式写入文件
#     """
#     with open(output_file, 'w') as file:
#         # 写入图的总信息
#         file.write(f"t {len(subgraph.nodes)} {len(subgraph.edges)}\n")
        
#         # 写入节点信息
#         for node in subgraph.nodes:
#             label = subgraph.nodes[node].get('label', '')  # 获取节点标签
#             degree = subgraph.degree[node]  # 计算节点度数
#             file.write(f"v {node} {label} {degree}\n")
        
#         # 写入边信息
#         for edge in subgraph.edges:
#             file.write(f"e {edge[0]} {edge[1]}\n")

# # 文件路径
# input_file = "HPRD.graph"  # 输入文件路径
# output_file = "renumbered_induced_subgraph.txt"  # 输出文件路径

# # 读取图
# G = read_graph_from_file(input_file)

# # 生成包含 24 个节点的连通诱导子图
# k = 24
# induced_subgraph = generate_connected_induced_subgraph(G, k)

# # 对子图节点重新编号
# renumbered_subgraph = renumber_subgraph(induced_subgraph)

# # 将重新编号后的子图写入文件
# write_subgraph_to_file(renumbered_subgraph, output_file)

# print(f"重新编号后的连通诱导子图已写入文件: {output_file}")

import networkx as nx
import random
import os

def read_graph_from_file(file_path):
    """
    从文件中读取图数据并构建图
    """
    G = nx.Graph()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == 't':
                # 图的总信息，可以忽略或记录
                vertex_number = int(parts[1])
                edge_number = int(parts[2])
            elif parts[0] == 'v':
                # 添加节点
                vertex_id = int(parts[1])
                vertex_label = parts[2]
                vertex_degree = int(parts[3])
                G.add_node(vertex_id, label=vertex_label, degree=vertex_degree)
            elif parts[0] == 'e':
                # 添加边
                source = int(parts[1])
                target = int(parts[2])
                elabel = int(parts[3])
                G.add_edge(source, target, label=elabel)
    return G

def find_connected_nodes(G, k):
    """
    从图中找到一个包含 k 个节点的连通子图
    """
    if k > len(G.nodes):
        raise ValueError("k 不能大于图的节点数")
    
    # 随机选择一个起始节点
    start_node = random.choice(list(G.nodes))
    
    # 使用 BFS 扩展连通节点
    visited = set()
    queue = [start_node]
    
    while queue and len(visited) < k:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            # 将邻居节点加入队列
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)
    
    # 如果找到的节点数不足 k，重新选择起始节点并重试
    if len(visited) < k:
        return find_connected_nodes(G, k)
    
    return list(visited)

def generate_connected_induced_subgraph(G, k):
    """
    生成包含 k 个节点的连通诱导子图
    """
    connected_nodes = find_connected_nodes(G, k)
    induced_subgraph = G.subgraph(connected_nodes)
    return induced_subgraph

def renumber_subgraph(subgraph):
    """
    对子图的节点重新编号，从 0 开始
    """
    # 创建节点映射字典
    node_mapping = {old_node: new_node for new_node, old_node in enumerate(subgraph.nodes)}
    
    # 重新编号节点
    renumbered_subgraph = nx.relabel_nodes(subgraph, node_mapping)
    
    return renumbered_subgraph

def write_subgraph_to_file(subgraph, output_file):
    """
    将诱导子图按照输入格式写入文件
    """
    with open(output_file, 'w') as file:
        # 写入图的总信息
        file.write(f"t {len(subgraph.nodes)} {len(subgraph.edges)}\n")
        
        # 写入节点信息
        for node in subgraph.nodes:
            label = subgraph.nodes[node].get('label', '')  # 获取节点标签
            degree = subgraph.degree[node]  # 计算节点度数
            file.write(f"v {node} {label} {degree}\n")
        
        # 写入边信息
        for edge in subgraph.edges:
            label = subgraph.edges[edge].get('label', '')  # 获取边标签
            file.write(f"e {edge[0]} {edge[1]} {label}\n")

def generate_subgraphs_for_sizes(G, sizes, groups_per_size, output_dir):
    """
    为指定大小的子图生成多组文件
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for size in sizes:
        for group in range(1, groups_per_size + 1):
            # 生成连通诱导子图
            induced_subgraph = generate_connected_induced_subgraph(G, size)
            
            # 重新编号子图节点
            renumbered_subgraph = renumber_subgraph(induced_subgraph)
            
            # 定义输出文件名
            output_file = os.path.join(output_dir, f"subgraph_size_{size}_group_{group}.txt")
            
            # 将子图写入文件
            write_subgraph_to_file(renumbered_subgraph, output_file)
            
            print(f"生成文件: {output_file}")

# 文件路径
input_file = "AIDS.graph"  # 输入文件路径
output_dir = "sub100"  # 输出文件夹路径

# 读取图
G = read_graph_from_file(input_file)

# 定义子图大小和每组数量
sizes = [5, 10, 24, 32, 64]  # 子图大小
groups_per_size = 100  # 每组生成 20 个子图

# 生成子图并保存
generate_subgraphs_for_sizes(G, sizes, groups_per_size, output_dir)

print("所有子图生成完成！")