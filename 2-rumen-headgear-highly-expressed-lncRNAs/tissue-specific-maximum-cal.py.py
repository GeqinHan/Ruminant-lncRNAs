#!/bin/python

import pandas as pd

# 文件路径
file_path = "tau-generate-output-file-v3-out-lncRNA.csv"  # 替换为实际文件路径

# 读取数据文件，指定分隔符为制表符
df = pd.read_csv(file_path, sep="\t")

# 筛选 tau 值大于 0.8 的行
filtered_df = df[df["tau"] > 0.8]

# 提取组织列
tissue_columns = df.columns[5:]

# 计算每行的最大 FPKM 值及其对应的组织名称
results = filtered_df.apply(
    lambda row: {
        "name": row["name"],
        "max_fpkm": row[tissue_columns].astype(float).max(),
        "tissue": tissue_columns[row[tissue_columns].astype(float).argmax()],
    },
    axis=1,
)

# 输出结果
print("Results:")
for result in results:
    print(f"Transcript: {result['name']}, Max FPKM: {result['max_fpkm']}, Tissue: {result['tissue']}")

