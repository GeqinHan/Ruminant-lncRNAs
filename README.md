# HomLncFinder Ruminant
**HomLncFinder** is a pipeline to identify lineage conserved lncRNAs through combination of genome alignment and lncRNA expression loci.

If this pipeline or files are helpful for your research please cite the following publication:
"Systematic identification of lncRNAs in ruminants and their important roles in rumen development" 

---
## 🐑 Example of usage
Here, we use sheep as the reference genome to show how to use the **HomLncFinder** pipeline to identify lineage conserved lncRNAs.

---
## 💻 Requirements

Ensure that the following dependencies and tools are installed to run the pipeline:
- python3.7
- cactus
- sra-tools
- hisat2
- samtools
- fasterq-dump
- fastp
- bowtie2
- stringtie
- gffcompare

---

### 1️⃣ Step 1. Genome and annotation files preparation.
Perapare FASTA and gff files for 4 Ruminant species in this study.
### 2️⃣ Step 2. RNA-seq data process.
Quality control and reads mapping. 
1. collect RNA-seq data
2. download FASTQ files with fasterq-dump
3. performe quality control of RNA-seq data
4. removal of rRNA
5. align RNA-seq data to the reference genome
6. screen and filter of lncRNAs

### 3️⃣ Step 3. LncRNAs identification.
Taking intersections of lncRNAs predicted by CPC, CPAT and CNCI.


### 4️⃣ Step 4. Rumen and headgear specific highly expressed (SHE) lncRNAs.
Rumen- and horn-specific highly expressed lncRNAs were screened using tau value ≥ 0.8 as cutoff value.


### 5️⃣ Step 5. Genome alignment.
A multi-species genome alignment of 14 Ungulate species using sheep as the reference genome.  
14 Species were listed in file [step5-genome-alignment/03.input-specieslist](https://github.com/hamgle/HomLncFinder-Ruminant/step5-genome-alignment/03.input-specieslist)
1. Get *.hal files of genome alignment between 14 species by **Cactus**.
    ```
    01.whole-genome-alignment
    ```
2. Extract the desired *.maf from *.hal.  
    ```
    # change the input and output file to your own path in the 01.hal2maf.sh file.

    bash 02.hal2maf.sh
    ```

3. Convert *.maf into the *.maflist. 
    ```
    # change the input and output file to your own path in the 02.maf2maflist.sh file.

    bash 03.maf2maflist.sh
    ```

### 6️⃣ Step 6. Candidate homologous lncRNA pairs.
Filter candidate homologous lncRNA pairs based on the following criteria: 
- Overlap length between lncRNA and homolog block ≥ 50bp;
- Bidirectional homolog block overlap ratio ≥ 40%.

1. make the file a standard format.
    ```
    python 01.check_block.py
    python 02.check_lncRNA_block.py
    ```
2. screen orthologous lncRNA pairs by bidirectional homolog block overlap ratio ≥ 40%。
    ```
    # The first three files are input, and the fourth file is the output!

    python 03.candidate-homologous-lncRNA.py 02.output-deer-lncRNA-block.txt 02.output-sheep-lncRNA-block.txt 01.output-sheep-deer-block.txt 03.output-deer-sheep-candidate-homolog.txt

    #The first two files are input, and the third file is the output!

    python 04.homologous-lncRNA-pairs.py 03.output-sheep-deer-candidate-homolog.txt 03.output-deer-sheep-candidate-homolog.txt 04.output-deer-sheep-homologous-lncRNA-pairs.txt

    ```

### 7️⃣ Step 7. Calculate whole genome identity value.

The genome sequence identity value between species is calculated based on 1v1 comparisons.
- <font style="color: #A8D8A8;">cutoff1</font>: Whole genome identity cutoff value by lesser mouse-deer;
- <font style="color: #A3C6FF;">cutoff2</font>: Whole genome identity cutoff value by rein deer.

    ```
    python 01.sheep-whole-genome-alignment-identity.py
    ```
     
 
### 8️⃣ Step 8. Calculate lncRNA identity value.

The Step8 involves keeping sheep rumen SHE lncRNAs identity value ≥ <font style="color: #A8D8A8;">cutoff1</font> in ruminant group and ≤ <font style="color: #A8D8A8;">cutoff1</font> in outgroup, and keeping sika deer antler SHE lncRNAs identity value ≥ <font style="color: #A3C6FF;">cutoff2</font> in cervidae group and ≤ <font style="color: #A3C6FF;">cutoff2</font> in outgroup. 

```
python 01.sheep-lncRNA-identity.py
```







