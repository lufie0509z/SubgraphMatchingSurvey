import os

# 定义日志文件所在的目录
log_directory = '.'  # 当前目录，你可以根据实际情况修改
output_file = 'atime.log'
output_file1 = 'aeps.log'

# 用于存储按 r 分组的结果
grouped_results = {}
grouped_results1 = {}

# 遍历目录中的所有文件
for filename in os.listdir(log_directory):
    if filename.endswith('.txt'):  # 只处理以.txt结尾的文件
        times = []
        # 打开当前日志文件
        with open(os.path.join(log_directory, filename), 'r') as infile:
            # 逐行读取文件
            for line in infile:

                if 'Per Embedding Count Time (nanoseconds):' in line:
                    # 提取时间值
                    time_str = line.split(':')[-1].strip()
                    time_ns = float(time_str)
                    times.append(time_ns)

        # 确保有 5 次实验结果
        print(f"Warning: {filename} ")
        if len(times) <= 50:
            print(f"Warning: {filename} has {len(times)} valid time entries.")
            if len(times) >= 3:
                # 对 times 列表进行排序
                sorted_times = sorted(times)
                # 去掉最高和最低值
                trimmed_times = sorted_times[1:-1]
                # 计算去掉最高和最低值后的平均值
                average_time_ns = sum(trimmed_times) / len(trimmed_times)
            else:
                # 如果元素数量小于 3，直接计算平均值
                average_time_ns = sum(times) / len(times)
    

            average_time_s = average_time_ns / 1e9  # 转换为秒
            eps = 1 / average_time_s
            print(f"{filename}: {average_time_s:.9f} seconds, {eps:.9f} eps")

            # 提取 r 的值
            parts = filename.split('_')
            r_value = parts[1]

            # 将结果添加到对应的分组中
            if r_value not in grouped_results:
                grouped_results[r_value] = []
            grouped_results[r_value].append((filename, average_time_s))
            if r_value not in grouped_results1:
                grouped_results1[r_value] = []
            grouped_results1[r_value].append((filename, eps))
        else:
            print(f"Warning: {filename} has {len(times)} valid time entries.")

# 打开输出文件以写入结果
with open(output_file, 'w') as outfile:
    # 按 r 的值排序
    sorted_r_values = sorted(grouped_results.keys(), key=lambda x: int(x))
    for r_value in sorted_r_values:
        outfile.write(f"Group r = {r_value}:\n")
        for filename, average_time_s in grouped_results[r_value]:
            outfile.write(f"{filename}:{average_time_s:.9f}\n")
        outfile.write("\n")

    
with open(output_file1, 'w') as outfile:
    # 按 r 的值排序
    sorted_r_values = sorted(grouped_results1.keys(), key=lambda x: int(x))
    for r_value in sorted_r_values:
        outfile.write(f"Group r = {r_value}:\n")
        for filename, eps in grouped_results1[r_value]:
            outfile.write(f"{filename}:{eps:.9f}\n")
        outfile.write("\n")