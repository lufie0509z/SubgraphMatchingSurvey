import os
import re

# 定义正则表达式来匹配 "Average Candidates Count: " 后面的数字
pattern = re.compile(r'Call Count: (\d+)')

# 初始化一个字典来存储每个方法的统计结果
method_stats = {}

# 遍历当前目录下的所有文件
for filename in os.listdir('.'):
    if filename.endswith('.txt') and '_' in filename:
        # 解析文件名以获取方法名
        parts = filename.split('_')
        if len(parts) >= 3:
            method = parts[2].split('.')[0]  # 获取方法名
            if method not in method_stats:
                method_stats[method] = {'total': 0, 'count': 0}

            # 打开文件并读取内容
            with open(filename, 'r') as file:
                for line in file:
                    match = pattern.search(line)
                    if match:
                        count = int(match.group(1))
                        method_stats[method]['total'] += count
                        if count != 0:
                            method_stats[method]['count'] += 1

# 输出统计结果
for method, stats in method_stats.items():
    print(f"Method: {method}")
    print(f"  Total Average Candidates Count: {stats['total']}")
    print(f"  Non-zero Count: {stats['count']}")
    print(f"  Average Non-zero Candidates Count: {stats['total'] / stats['count']:.2f}")
    print()