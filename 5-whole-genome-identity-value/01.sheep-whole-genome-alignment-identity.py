import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

template_inputdir = '~/3-genome-alignment'
template_inputfile = '~/01.input-species-list' 
template_intermediate_dir = '~/whole_genome_analysis/tmp'
output_dir = '~/whole_genome_analysis/csv'

chromosomes = [f'chr{i}' for i in range(1, 27)] + ['chrX']


def read_species_list(template_inputfile):
    with open(template_inputfile, 'r') as file:
        return [line.strip() for line in file.readlines()]

species_list = read_species_list(os.path.expanduser(template_inputfile))

for chr_name in chromosomes:
    script_name = f'{template_intermediate_dir}/{chr_name}_process.py'
    bash_name = f'{template_intermediate_dir}/{chr_name}_process.sh'

    chr_files = sorted([f for f in os.listdir(template_inputdir) if f.startswith(f'14sp.{chr_name}.') and f.endswith('.maflist')])
    num_files = len(chr_files)

    with open(script_name, 'w') as py_script:
        py_script.write(f'''import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os

file_paths = [f'{template_inputdir}/{{file}}' for file in {chr_files}]

identity_output_file = '{output_dir}/{chr_name}_identity_score.csv'
base_matching_output_file = '{output_dir}/{chr_name}_base_matching_counts.csv'

species_list = {species_list}

identity_scores_per_chr = {{species: [] for species in species_list}}
chromosome_labels = []
genome_total_bases = {{species: 0 for species in species_list}}
genome_matching_bases = {{species: 0 for species in species_list}}
base_counts_per_chr = {{species: [] for species in species_list}}
total_bases_per_chr = []

def process_file(file_path):
    chr_segment = file_path.split('.')[-2]
    chromosome_labels.append(chr_segment)

    df = pd.read_csv(file_path, sep='\\t', header=0, dtype={{'pos': 'str'}}, low_memory=False)
    df_filtered = df[df['pos'] != '-'] 

    total_bases = len(df_filtered)
    if total_bases == 0:
        return

    total_bases_per_chr.append(total_bases)

    for species in species_list:
        if species == 'sheep':
            identity_scores_per_chr[species].append(1.0)
            base_counts_per_chr[species].append(total_bases)
        else:
            matching_bases = (df_filtered[species].str.upper() == df_filtered['sheep'].str.upper()).sum()
            identity_scores_per_chr[species].append(matching_bases / total_bases)
            base_counts_per_chr[species].append(matching_bases)

            genome_total_bases[species] += total_bases
            genome_matching_bases[species] += matching_bases

    if not os.path.exists(identity_output_file):
        identity_df = pd.DataFrame(identity_scores_per_chr)
        identity_df['chr'] = chromosome_labels
        identity_df = identity_df[['chr'] + species_list]
        identity_df.to_csv(identity_output_file, mode='a', header=True, index=False) 
    else:
        identity_df = pd.DataFrame(identity_scores_per_chr)
        identity_df['chr'] = chromosome_labels
        identity_df = identity_df[['chr'] + species_list]
        identity_df.to_csv(identity_output_file, mode='a', header=False, index=False)

    if not os.path.exists(base_matching_output_file):
        base_counts_df = pd.DataFrame(base_counts_per_chr)
        base_counts_df['chr'] = chromosome_labels
        base_counts_df['total_bases'] = total_bases_per_chr
        base_counts_df = base_counts_df[['chr', 'total_bases'] + species_list]
        base_counts_df.to_csv(base_matching_output_file, mode='a', header=True, index=False)
    else:
        base_counts_df = pd.DataFrame(base_counts_per_chr)
        base_counts_df['chr'] = chromosome_labels
        base_counts_df['total_bases'] = total_bases_per_chr
        base_counts_df = base_counts_df[['chr', 'total_bases'] + species_list]
        base_counts_df.to_csv(base_matching_output_file, mode='a', header=False, index=False)

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_file, file_paths)

chromosome_labels.append('whole')
total_bases_per_chr.append(sum(total_bases_per_chr))

for species in species_list:
    genome_identity = genome_matching_bases[species] / genome_total_bases[species] if genome_total_bases[species] > 0 else 0
    identity_scores_per_chr[species].append(genome_identity)
    base_counts_per_chr[species].append(genome_matching_bases[species])

identity_df = pd.DataFrame(identity_scores_per_chr)
identity_df['chr'] = chromosome_labels
identity_df = identity_df[['chr'] + species_list]
identity_df.to_csv(identity_output_file, mode='a', header=True, index=False)

base_counts_df = pd.DataFrame(base_counts_per_chr)
base_counts_df['chr'] = chromosome_labels
base_counts_df['total_bases'] = total_bases_per_chr
base_counts_df = base_counts_df[['chr', 'total_bases'] + species_list]
base_counts_df.to_csv(base_matching_output_file, mode='a', header=True, index=False)
''')

    with open(bash_name, 'w') as bash_script:
        bash_script.write(f'''#!/bin/bash
python {script_name}
''')

print("All scripts generated successfully.")
