import os
from collections import defaultdict

def convert_to_graph_format(node_labels_file, edges_file, link_labels_file, output_file):


    # 读取节点标签
    with open(node_labels_file, "r") as f:
        node_labels = [int(line.strip().split(",")[1]) for line in f]

    with open(link_labels_file, "r") as f:
        link_labels = [int(line.strip()) for line in f]

    with open(edges_file, "r") as f:
        edges = [tuple(map(int, line.strip().split(","))) for line in f]
    # with open(edges_file, "r") as f:
    #   edges_set = set()  # 用于存储唯一的边
    #   for line in f:
    #       edge = tuple(sorted(map(int, line.strip().split(","))))  # 排序确保无向边一致性
    #       edges_set.add(edge)

    # edges = list(edges_set)  # 转换为列表供后续使用

    vertices = defaultdict(lambda: {"label": 0, "degree": 0})
    edge_list = []

    max_vertex_degree = 0

    for edge, label in zip(edges, link_labels):
        src, dst = edge

        # 更新节点信息
        # print(src, dst)
        vertices[src]["label"] = node_labels[src - 1]
        vertices[src]["degree"] += 1
        vertices[dst]["label"] = node_labels[dst - 1]
        vertices[dst]["degree"] += 1

        max_vertex_degree = max(max_vertex_degree, vertices[src]["degree"], vertices[dst]["degree"])

        # 添加边
        edge_list.append((src, dst, label))
    

    with open(output_file, "w") as f:
        f.write(f"t {len(vertices)} {len(edge_list)}\n")
        for vertex_id, data in vertices.items():
            f.write(f"v {vertex_id} {data['label']} {data['degree']}\n")
        for src, dst, label in edge_list:
            f.write(f"e {src} {dst} {label}\n")

    print(f"Graph file saved to {output_file}")
    print(f"max_vertex_degree: {max_vertex_degree}")

# 使用示例
node_labels_file = "AIDS.node_labels"  # 替换为实际路径
edges_file = "AIDS.edges"             # 替换为实际路径
link_labels_file = "AIDS.link_labels" # 替换为实际路径
output_file = "AIDS.graph"                 # 输出文件路径

convert_to_graph_format(node_labels_file, edges_file, link_labels_file, output_file)