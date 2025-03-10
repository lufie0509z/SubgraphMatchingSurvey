from collections import defaultdict

# 原始数据
data = """
Group r = 5:
size_5_QSI.txt:6264602.396648939
size_5_best.txt:40872.471227784
size_5_RM.txt:452.368181357
size_5_our.txt:2865798.387071352
size_5_VEQ.txt:165325.373188483
size_5_CFL.txt:3053989.287928973
size_5_CECI.txt:3205557.667661886

Group r = 10:
size_10_our.txt:476646.805736973
size_10_CECI.txt:950903.147008022
size_10_RM.txt:6233.506580126
size_10_CFL.txt:601514.713298012
size_10_best.txt:33035.042055643
size_10_VEQ.txt:402482.924202859
size_10_QSI.txt:978718.578079480

Group r = 24:
size_24_CFL.txt:718436.026842437
size_24_best.txt:25352.991376457
size_24_RM.txt:6624.858392182
size_24_VEQ.txt:637881.067279128
size_24_QSI.txt:1251254.177028583
size_24_our.txt:541007.428976959
size_24_CECI.txt:1710412.891055975

Group r = 32:
size_32_best.txt:19725.067843919
size_32_QSI.txt:1557987.807644427
size_32_VEQ.txt:750432.493006532
size_32_CFL.txt:764085.597664757
size_32_CECI.txt:1908777.654818032
size_32_RM.txt:6616.943683687
size_32_our.txt:608225.332476553

Group r = 64:
size_64_RM.txt:7515.260324785
size_64_best.txt:37537.234625863
size_64_QSI.txt:3234612.016195487
size_64_our.txt:1323886.169884118
size_64_CFL.txt:1253317.020994533
size_64_VEQ.txt:780086.553723482
size_64_CECI.txt:3450229.643834864
"""

# 初始化字典来存储分类结果
method_data = defaultdict(dict)

# 解析数据
current_group = None
for line in data.splitlines():
    if line.startswith("Group r ="):
        current_group = line.split("=")[1].strip().rstrip(":")
    elif line.strip() and ":" in line:
        filename, value = line.split(":")
        method = filename.split("_")[2].split(".")[0]
        method_data[method][current_group] = float(value.strip())

# 输出分类结果
for method, values in method_data.items():
    print(f"方法：{method}")
    for group, value in values.items():
        print(f"  Group r = {group}: {value}")
    print()