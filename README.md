
This is a pipeline to identify lineage specific lncRNAs through combination of genome alignment and lncRNAs expression.

If this pipeline or files are helpful for your research please cite the following publication:
"Systematic identification of lncRNAs in ruminants and their important roles in rumen development" 

---


## 🐑 Example 
Here, we use sheep as the reference genome to show how to use this pipeline to identify lineage specific lncRNAs.

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

Rumen- and horn/antler highly expressed lncRNAs were screened using tau value ≥ 0.8 and fpkm ≥ 1 as cutoff values.

```
# 2-rumen-headgear-highly-expressed-lncRNAs
```


### 3️⃣ Step 3. Genome alignment.
A multi-species genome alignment of 14 Ungulate species using sheep/sika deer as the reference genome. 

```
# 3-genome-alignment
```


### 4️⃣ Step 4. Candidate homologous lncRNA pairs.
Filtering candidate homolog lncRNA pairs based on the following criteria:

- 1) Overlap length between lncRNA and homolog block ≥ 50bp;
- 2) Bidirectional homolog block overlap ratio ≥ 40%.

```
# 4-candidate-homolog-lncRNA-pairs
```


### 5️⃣ Step 5. Calculate whole genome identity value.

The genome sequence identity value between species is calculated based on 1v1 comparisons.

```
# 5-whole-genome-identity-value
```

 
### 6️⃣ Step 6. Calculate lncRNA identity value.

The step6 involves keeping lncRNAs with identity value ≥ cutoff in innergroup and < cutoff in outgroup. The cutoff value equals the 1v1 whole genome identity value.

```
# 6-lncRNAs-identity-value
```







