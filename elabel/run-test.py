import os
import subprocess
from itertools import product

# 定义参数的可选范围
query_directory = "./zxy_data_set/telecom/subgraph3"  # 替换为实际的目录路径
# 获取 query_files
query_files = [
    os.path.join(query_directory, file)
    for file in os.listdir(query_directory)
    if os.path.isfile(os.path.join(query_directory, file))
]

print("Query files:", query_files)



filters = ["LDF", "NLF", "CFL", "CECI", "DPiso", "RM", "VEQ"]  # 替换为实际的 filter 参数可选值
orders =  ["CFL", "CECI", "DPiso", "RM"]  # 替换为实际的 order 参数可选值
engines = ["CECI", "RM", "VEQ", "RM"]  # 替换为实际的 engine 参数可选值

# 定义固定的参数
dataset_path = "./zxy_data_set/telecom/telecom.graph"
num_value = "MAX"
executable = "./build/matching/SubgraphMatching.out"

error_log_file = "error_log.txt"

# 遍历参数组合
for query_file, filter_value, order_value, engine_value in product(query_files, filters, orders, engines):
    # 构造命令
    command = [
        "time",
        executable,
        "-d", dataset_path,
        "-q", query_file,
        "-filter", filter_value,
        "-order", order_value,
        "-engine", engine_value,
        "-num", num_value,
    ]
    
    # 打印当前执行的命令
    print("Running command:", " ".join(command))
    try:
    # 执行命令
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        output_dir = os.path.join("telecomresult", os.path.basename(query_file))
        os.makedirs(output_dir, exist_ok=True)  # 确保目录存在
    
        # 将结果保存到文件
        output_file = os.path.join(
            output_dir, f"{filter_value}_{order_value}_{engine_value}.txt"
        )
        with open(output_file, "w") as f:
            f.write(result.stdout)
            f.write("\n")
            f.write(result.stderr)
        
        print(f"Result saved to {output_file}")
    except subprocess.CalledProcessError as e:
        # 捕获命令执行失败的异常，记录到日志文件中
        with open(error_log_file, "a") as log:
            log.write(f"Command failed: {' '.join(command)}\n")
            log.write(f"Error output: {e.stderr}\n\n")
        print(f"Command failed. See {error_log_file} for details.")
    except Exception as e:
        # 捕获其他异常，记录到日志文件中
        with open(error_log_file, "a") as log:
            log.write(f"Unexpected error with command: {' '.join(command)}\n")
            log.write(f"Error: {str(e)}\n\n")
        print(f"Unexpected error. See {error_log_file} for details.")



print("All tasks completed.")