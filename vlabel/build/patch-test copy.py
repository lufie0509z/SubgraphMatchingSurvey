import subprocess
import os
import re

# 配置
executable = "./matching/SubgraphMatching.out"  # 可执行文件路径
data_file = "/home/ubuntu/zxy/SubgraphMatchingSurvey/vlabel/test/telecom/telecom.graph"  # 数据文件路径
query_files_list = "/home/ubuntu/zxy/SubgraphMatchingSurvey/vlabel/test/telecom/sub2/enum.txt"  # 包含所有查询数据集的文件路径
# output_dir = "/home/ubuntu/zxy/SubgraphMatchingSurvey/vlabel/test/HPRD/data2"  # 结果输出目录

# 配对的参数组合
filters = ["VEQ", "RM", "DPiso", "DPiso", "CFL",  "NLF", "CECI"]  # -filter 参数选项
orders =  ["RI",  "RM", "DPiso", "RM",    "CFL",  "QSI", "CECI"]  # -order 参数选项
engines = ["VEQ", "RM", "DPiso", "VEQ",   "LFTJ", "QSI", "CECI"]  # -engine 参数选项
logdirs = ["VEQ", "RM", "our",   "best",  "CFL",  "QSI", "CECI"]  # -logdir 参数选项

# 检查参数长度是否一致
if not (len(filters) == len(orders) == len(engines) == len(logdirs)):
    raise ValueError("参数列表长度不一致！")

# 创建日志目录
logdir = "telecom_main_experiment_200"
os.makedirs(logdir, exist_ok=True)
# for logdir in logdirs:
#     os.makedirs(logdir, exist_ok=True)

# 读取查询数据集文件
base_directory = "/home/ubuntu/zxy/SubgraphMatchingSurvey/vlabel/test/telecom/sub2"
with open(query_files_list, 'r') as file:
    query_files = [os.path.join(base_directory, line.strip()) for line in file if line.strip()]

# 按 size 分组
size_to_files = {}
for query_file in query_files:
    # 从文件名中提取 size 值
    match = re.search(r"subgraph_size_(\d+)_group_\d+\.txt", query_file)
    if not match:
        raise ValueError(f"文件名格式不正确：{query_file}")
    size = match.group(1)
    if size not in size_to_files:
        size_to_files[size] = []
    size_to_files[size].append(query_file)




# 遍历每个 size 组
for size, files in size_to_files.items():
    # 遍历所有配对的参数组合
    for filter_param, order_param, engine_param, logdir_param in zip(filters, orders, engines, logdirs):
        # 构造输出文件名
        output_file = os.path.join(
            logdir,  # 日志保存到对应的 logdir 目录
            f"size_{size}_{logdir_param}.txt"
        )
        
        # 打开输出文件（追加模式）
        with open(output_file, 'a') as f:
            # 遍历当前 size 组的所有查询文件
            for query_file in files:
                # 构造命令
                command = [
                    "/usr/bin/time", "-v",
                    executable,
                    "-d", data_file,
                    "-q", query_file,
                    "-filter", filter_param,
                    "-order", order_param,
                    "-engine", engine_param,
                    "-num", "MAX"
                ]
                
                # 打印当前运行的命令
                print(f"Running: {' '.join(command)}")
                
                # 运行命令并将结果追加到文件
                f.write(f"Results for query file: {query_file}\n")
                f.write("=" * 50 + "\n")
                subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)
                f.write("\n\n")  # 添加分隔符
        
        print(f"Results for size {size} saved to: {output_file}")

print("All tests completed!")