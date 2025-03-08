import networkx as nx
import random

# 创建一个空的无向图
G = nx.Graph()

# 打开数据集文件
with open('HPRD.graph', 'r') as file:
    for line in file:
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] == 't':
            # 这行是图的元数据，可以忽略或记录
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
            edge_label = 0
            G.add_edge(source, target, label=edge_label)

# 现在你可以使用 networkx 的各种功能来分析和操作这个图
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

def generate_connected_subgraph(G, size):
    """
    从图 G 中生成一个包含指定节点数的连通子图
    :param G: 原始图
    :param size: 子图的节点数
    :return: 连通子图
    """
    if size > G.number_of_nodes():
        raise ValueError("子图大小不能超过原图的节点数")

    # 随机选择一个起始节点
    start_node = random.choice(list(G.nodes()))
    visited = set()
    queue = [start_node]

    while len(visited) < size and queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            # 将邻居加入队列
            queue.extend([n for n in G.neighbors(node) if n not in visited])

    # 提取子图
    subgraph = G.subgraph(visited).copy()
    return subgraph

def save_subgraph_to_file(subgraph, filename):
    """
    将子图按照指定格式保存到文件
    :param subgraph: 子图
    :param filename: 输出文件名
    """
    with open(filename, 'w') as file:
        # 写入图的元数据
        file.write(f"t {subgraph.number_of_nodes()} {subgraph.number_of_edges()}\n")

        # 写入节点信息
        for node, attr in subgraph.nodes(data=True):
            node_label = attr.get('label', '')  # 如果没有标签，默认为空
            node_degree = subgraph.degree(node)  # 计算节点的度
            file.write(f"v {node} {node_label} {node_degree}\n")

        # 写入边信息
        for source, target, attr in subgraph.edges(data=True):
            edge_label = attr.get('label', '')  # 如果没有标签，默认为空
            file.write(f"e {source} {target} {edge_label}\n")


def generate_multiple_subgraphs(G, node_sizes, num_subgraphs_per_size):
    """
    为每个节点个数生成多组随机连通子图
    :param G: 原始图
    :param node_sizes: 节点个数的集合（列表）
    :param num_subgraphs_per_size: 每组节点个数生成的子图数量
    """
    for size in node_sizes:
        for i in range(num_subgraphs_per_size):
            # 生成随机连通子图
            subgraph = generate_connected_subgraph(G, size)

            # 保存到文件
            filename = f"sub2/subgraph_size_{size}_group_{i + 1}.txt"
            save_subgraph_to_file(subgraph, filename)

            print(f"子图已保存到文件：{filename}")

# 示例：生成随机连通子图并保存到文件
# 假设 G 是你的原始图
node_sizes = [4, 8, 12, 16, 32, 64]  # 指定的节点个数集合
num_subgraphs_per_size = 10  # 每组节点个数生成 10 组子图

generate_multiple_subgraphs(G, node_sizes, num_subgraphs_per_size)