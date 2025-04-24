
This is a pipeline to identify lineage specific lncRNAs through combination of genome alignment and bootstrap algorithm.

If this pipeline or files are helpful for your research please cite the following publication:
"Systematic identification of lncRNAs in ruminants and their important roles in rumen development".

---


## 🐑 Example 
Here, we use sheep as the reference species to show how to use this pipeline to identify lineage specific lncRNAs.

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


### 3️⃣ Step 3. Genome alignment.
A multi-species genome alignment was performed across 14 ungulate species, using the sheep (or sika deer) genome as the reference. 

```
# 3-genome-alignment
```


### 4️⃣ Step 4. Calculate lncRNAs sequence identity.
Calculate sequence identity for lncRNAs in the reference species (sheep or sika deer) by comparing them against multiple other species based on genome alignment data.

```
# 4-lncRNAs-sequence-identity
```


### 5️⃣ Step 5.Calculate mRNAs sequence identity.

Calculate sequence identity for mRNAs in the reference species (sheep or sika deer) by comparing them against multiple other species based on genome alignment data.

```
# 5-mRNAs-sequence-identity
```

 
### 6️⃣ Step 6. Calculate lncRNA identity value.

Calculate sequence identity between sheep mRNAs and multiple other species, and compute bootstrap confidence intervals (CI) for these identity values. 

```
# 6-bootstrap-algorithm
```







