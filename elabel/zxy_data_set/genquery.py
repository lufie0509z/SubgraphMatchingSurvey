import random
import networkx as nx


def read_graph(input_file):
    """读取图文件并构建 NetworkX 图对象"""
    G = nx.Graph()
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if parts[0] == 't':  # 图元信息
                vertex_count = int(parts[1])
                edge_count = int(parts[2])
            elif parts[0] == 'v':  # 顶点信息
                vertex_id = int(parts[1])
                vertex_label = int(parts[2])
                G.add_node(vertex_id, label=vertex_label)
            elif parts[0] == 'e':  # 边信息
                src = int(parts[1])
                tgt = int(parts[2])
                edge_label = int(parts[3])
                G.add_edge(src, tgt, label=edge_label)
    return G


def random_walk_connected_induced_subgraph(G, node_count=10):
    """利用随机游走生成指定大小的联通诱导子图"""
    if len(G.nodes) < node_count:
        raise ValueError("Graph does not have enough nodes for the induced subgraph")

    # 从图中随机选择一个起始节点
    start_node = random.choice(list(G.nodes))
    induced_nodes = set([start_node])

    # 随机游走直到选出足够的节点
    while len(induced_nodes) < node_count:
        current_node = random.choice(list(induced_nodes))
        neighbors = list(G.neighbors(current_node))
        if neighbors:
            next_node = random.choice(neighbors)
            induced_nodes.add(next_node)

    # 构建诱导子图
    induced_subgraph = G.subgraph(induced_nodes).copy()
    return induced_subgraph


def write_graph_with_reordered_labels(output_file, G):
    """将诱导子图写入文件，节点标签重新排序从0开始"""
    # 创建原图ID到新标签的映射
    id_to_new_label = {old_id: new_id for new_id, old_id in enumerate(G.nodes())}

    with open(output_file, 'w') as file:
        # 写图元信息
        file.write(f"t {len(G.nodes)} {len(G.edges)}\n")
        
        # 写顶点信息
        for node in G.nodes(data=True):
            original_id, attrs = node
            new_id = id_to_new_label[original_id]
            label = attrs.get('label', -1)
            degree = G.degree(original_id)  # 重新计算子图中的实际度数
            file.write(f"v {new_id} {label} {degree}\n")
        
        # 写边信息
        for edge in G.edges(data=True):
            src, tgt, attrs = edge
            new_src = id_to_new_label[src]
            new_tgt = id_to_new_label[tgt]
            label = attrs.get('label', -1)
            file.write(f"e {new_src} {new_tgt} {label}\n")


def main():
    input_file = "AIDS.graph"       # 输入图文件名
    sizes = [32]  # 子图大小列表
    num_per_size = 20               # 每个大小生成的子图数量

    # 读取图
    graph = read_graph(input_file)

    # 遍历每种大小生成对应数量的子图
    for size in sizes:
        for i in range(0, 9 + num_per_size):  # 从 3 开始编号
            try:
                # 生成联通的诱导子图
                induced_subgraph = random_walk_connected_induced_subgraph(graph, node_count=size)
                output_file = f"subgraph3/subgraph_size_{size}_R{i + 1}.graph"
                
                # 写入带重新排序节点的诱导子图
                write_graph_with_reordered_labels(output_file, induced_subgraph)
                print(f"Generated reordered induced subgraph written to {output_file}")
            except ValueError as e:
                print(f"Failed to generate subgraph of size {size}: {e}")


if __name__ == "__main__":
    main()