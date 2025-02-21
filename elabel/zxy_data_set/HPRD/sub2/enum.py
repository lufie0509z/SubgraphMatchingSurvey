import os

def save_filenames_to_txt(directory, output_file):
    """
    将某个目录下的所有文件名保存到一个文本文件中
    :param directory: 目标目录路径
    :param output_file: 输出文件名
    """
    # 获取目录下的所有文件名
    filenames = os.listdir(directory)
    
    # 过滤掉子目录（只保留文件）
    filenames = [f for f in filenames if os.path.isfile(os.path.join(directory, f))]
    
    # 将文件名写入输出文件
    with open(output_file, 'w') as file:
        for filename in filenames:
            file.write(f"{filename}\n")
    
    print(f"文件名已保存到文件：{output_file}")

# 示例：将某个目录的文件名保存到 txt 文件
directory_path = "/home/ubuntu/zxy/SubgraphMatchingSurvey/elabel/zxy_data_set/HPRD/sub2"  # 替换为你的目录路径
output_txt_file = "enum.txt"  # 输出文件名

save_filenames_to_txt(directory_path, output_txt_file)