
This repository provides the lncRNA identification pipeline and associated lncRNA data for representative ruminant species.

If this pipeline or files are helpful for your research please cite the following publication:
"Systematic identification of lncRNAs in ruminants and their important roles in rumen development".

---

## 💻 Requirements

Ensure that the following dependencies and tools are installed to run the pipeline:
- python 3.8
- cactus
- sra-tools
- hisat2
- samtools
- fasterq-dump
- fastp
- bowtie2
- stringtie
- gffcompare



### 1️⃣ Step 1. RNA-seq data process.

Prepare genome and annotation files of 4 ruminant species in this study.

Quality control and reads mapping.

Taking the intersection of lncRNAs predicted by CPC, CPAT and CNCI.

```
# 1-RNA-seq-data-process
```
     
 
### 2️⃣ Step 2. Rumen and headgear highly expressed lncRNAs.

LncRNAs with high expression in the rumen and horn/antler were identified using a tau value ≥ 0.8 and an fpkm ≥ 1 as cutoff thresholds.

```
# 2-rumen-headgear-highly-expressed-lncRNAs
```










