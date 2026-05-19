#!/bin/bash

###"ID" represents RNA-seq data collected from SRA database (Supplementary Table1)###

fasterq-dump -e 20 -p -o ${ID}-fastq ${ID}

fastp -i ${ID}-fastq_1.fastq -I ${ID}-fastq_2.fastq -o ${ID}-fastq_1_out.fastq -O ${ID}-fastq_2_out.fastq -M 40 -l 50

bowtie2 -x species-rRNA-ID --un-conc-gz  ${i}_input_rmrRNA.fastq.gz -1 ${i}-fastq_1_out.fastq -2 ${i}-fastq_2_out.fastq -p 8 -S ${i}_rRNA.sam
