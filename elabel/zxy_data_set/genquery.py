import random
from collections import defaultdict

def load_graph(file_path):
    """加载图数据"""
    vertices = {}  # 节点信息 {vertex_id: (label, degree)}
    edges = defaultdict(list)  # 边信息 {vertex_id: [(target, edge_label)]}

    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == "v":  # 节点信息
                vertex_id = int(parts[1])
                vertex_label = int(parts[2])
                vertex_degree = int(parts[3])
                vertices[vertex_id] = (vertex_label, vertex_degree)
            elif parts[0] == "e":  # 边信息
                source = int(parts[1])
                target = int(parts[2])
                edge_label = int(parts[3])
                edges[source].append((target, edge_label))
                edges[target].append((source, edge_label))  # 无向图

    return vertices, edges

def random_walk_induced_subgraph(vertices, edges, start_node, target_size):
    """通过随机游走生成诱导子图"""
    visited = set()  # 存储已访问的节点
    subgraph_edges = set()  # 存储子图的边
    queue = [start_node]  # 随机游走队列

    while len(visited) < target_size and queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        # 遍历当前节点的邻居
        for neighbor, edge_label in edges[current]:
            if neighbor not in visited and len(visited) < target_size:
                queue.append(neighbor)
            # 添加边到子图
            if current < neighbor:  # 确保边的方向一致
                subgraph_edges.add((current, neighbor, edge_label))
            else:
                subgraph_edges.add((neighbor, current, edge_label))

    # 生成诱导子图的节点和边
    subgraph_vertices = {v: vertices[v] for v in visited}
    return subgraph_vertices, subgraph_edges

def generate_induced_subgraphs(file_path, sizes, num_subgraphs, output_dir):
    """生成指定大小和数量的诱导子图"""
    vertices, edges = load_graph(file_path)

    for size in sizes:
        for i in range(num_subgraphs):
            # 随机选择一个起始节点
            start_node = random.choice(list(vertices.keys()))
            subgraph_vertices, subgraph_edges = random_walk_induced_subgraph(vertices, edges, start_node, size)

            # 输出子图到文件
            output_file = f"{output_dir}/subgraph_{size}_{i}.graph"
            with open(output_file, "w") as f:
                f.write(f"t {len(subgraph_vertices)} {len(subgraph_edges)}\n")
                for v, (label, degree) in subgraph_vertices.items():
                    f.write(f"v {v} {label} {degree}\n")
                for src, tgt, label in subgraph_edges:
                    f.write(f"e {src} {tgt} {label}\n")

            print(f"Generated subgraph {size}_{i} at {output_file}")

# 使用示例
file_path = "./AIDS/AIDS.graph"  # 替换为你的数据集路径
sizes = [4, 8, 12, 16, 24, 32, 40]        # 子图点数
num_subgraphs = 20                        # 每种点数生成的子图数量
output_dir = "./AIDS/querygraph"           # 输出子图目录

import os
os.makedirs(output_dir, exist_ok=True)    # 确保输出目录存在
generate_induced_subgraphs(file_path, sizes, num_subgraphs, output_dir)