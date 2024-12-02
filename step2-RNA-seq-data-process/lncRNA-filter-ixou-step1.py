#!/bin/python

# 文件路径定义
transcript_ids_file = 'species-gffcompare.annotated.ixou.transcript.ID'
input_gtf_file = 'species-gffcompare.annotated.gtf'
output_gtf_file_step1 = 'species-gffcompare.annotated.ixou.transcript.gtf'

def save_matching_transcripts(transcript_ids_file, input_gtf_file, output_gtf_file_step1):
    # 读取transcript_ids并创建一个快速查找的集合
    with open(transcript_ids_file, 'r') as f:
        transcript_ids = {line.strip() for line in f}

    # 初始化列表来存储匹配的行
    matched_lines = []

    # 读取GTF文件并记录匹配的行
    with open(input_gtf_file, 'r') as infile:
        for line in infile:
            # 对每个transcript_id进行匹配检查
            for tid in transcript_ids:
                if tid in line:  # 直接检查整个transcript_id "X"是否在行中
                    matched_lines.append(line)
                    break  # 如果找到匹配，则不需要检查其他transcript_id

    # 写入所有匹配的transcript_id行到输出文件
    with open(output_gtf_file_step1, 'w') as outfile:
        outfile.writelines(matched_lines)

# 应用函数
save_matching_transcripts(transcript_ids_file, input_gtf_file, output_gtf_file_step1)
