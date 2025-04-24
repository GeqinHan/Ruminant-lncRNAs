#!/usr/bin/env python3

import os
import csv
import argparse
from collections import defaultdict
from intervaltree import IntervalTree
from multiprocessing import Pool, cpu_count

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate sequence identity for protein-coding genes from GFF3.')
    parser.add_argument('input_gff3', help='Path to the input GFF3 file containing protein-coding genes')
    parser.add_argument('input_maflist_dir', help='Directory containing MAFLIST files from genome alignment')
    parser.add_argument('output_dir', help='Directory to save output CSV files')
    return parser.parse_args()

def parse_gff3(gff3_file):
    """Parse GFF3 file and group exons by gene_id"""
    genes = defaultdict(lambda: {'chrom': None, 'strand': None, 'exons': []})
    
    with open(gff3_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            
            fields = line.strip().split('\t')
            if len(fields) < 9:
                continue
                
            chrom = fields[0]
            feature_type = fields[2]
            start = int(fields[3])
            end = int(fields[4])
            strand = fields[6]
            attributes = fields[8]
            
            # Parse attributes in GFF3 format (key=value pairs separated by ;)
            attr_dict = {}
            for attr in attributes.split(';'):
                if '=' in attr:
                    key, value = attr.split('=', 1)
                    attr_dict[key] = value
                    
            gene_id = attr_dict.get('gene_id') or attr_dict.get('Parent')  # GFF3 may use Parent
            if not gene_id:
                continue
                
            if feature_type == 'exon':
                if not genes[gene_id]['chrom']:
                    genes[gene_id]['chrom'] = chrom
                    genes[gene_id]['strand'] = strand
                genes[gene_id]['exons'].append({'start': start, 'end': end})
    
    return genes

def process_gene(args):
    """Process each gene to calculate sequence identity"""
    gene_id, data, maflist_dir, species_order = args
    chrom = data['chrom']
    exons = data['exons']
    
    # Format chromosome name for MAFLIST file
    chrom_formatted = f"chr{chrom}" if not chrom.startswith('chr') else chrom
    
    maflist_file = os.path.join(maflist_dir, 
                               f"14sp.{chrom_formatted}.sheep_ref.hal2maf.maf.sort.maf.list")
    
    if not os.path.exists(maflist_file):
        print(f"Warning: MAFLIST file {maflist_file} not found")
        return None
    
    # Build exon interval tree
    exon_tree = IntervalTree()
    for exon in exons:
        exon_tree[exon['start']:exon['end']+1] = True
    
    species_match_counts = {species: 0 for species in species_order[1:]}
    total_bases = 0
    
    try:
        with open(maflist_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            
            for row in reader:
                pos = int(row['pos'])
                sheep_base = row['sheep'].upper()
                
                if sheep_base == '-' or sheep_base not in {'A', 'T', 'C', 'G'}:
                    continue
                    
                if not exon_tree.overlaps(pos):
                    continue
                    
                total_bases += 1
                for species in species_order[1:]:
                    if species in row:
                        species_base = row[species].upper()
                        if species_base == sheep_base and species_base in {'A', 'T', 'C', 'G'}:
                            species_match_counts[species] += 1
    except Exception as e:
        print(f"Error processing {maflist_file}: {str(e)}")
        return None
        
    if total_bases == 0:
        print(f"No valid bases found for gene {gene_id}")
        return None
        
    # Calculate results
    identity_dict = {'Gene_id': gene_id}
    base_count_dict = {'Gene_id': gene_id}
    
    for species in species_order[1:]:
        match_count = species_match_counts[species]
        identity_dict[species] = round(match_count / total_bases, 4) if total_bases > 0 else 0
        base_count_dict[species] = match_count
    
    return gene_id, identity_dict, base_count_dict

def main():
    args = parse_arguments()
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    species_order = ['Gene_id', 'sheep', 'camel', 'pig', 'lesser_mouse_deer', 'pronghorn', 'giraffe',
                   'forest_musk_deer', 'cattle', 'goat', 'sika_deer', 'reindeer', 'hippo', 'killer_whale', 'tapir']
    
    genes = parse_gff3(args.input_gff3)
    
    identity_csv = os.path.join(args.output_dir, 'protein_gene_identity.csv')
    base_count_csv = os.path.join(args.output_dir, 'protein_gene_base_counts.csv')
    
    with open(identity_csv, 'w', newline='') as id_file, open(base_count_csv, 'w', newline='') as bc_file:
        id_writer = csv.DictWriter(id_file, fieldnames=species_order)
        bc_writer = csv.DictWriter(bc_file, fieldnames=species_order)
        id_writer.writeheader()
        bc_writer.writeheader()
        
        with Pool(cpu_count()) as pool:
            args_list = [(gene_id, data, args.input_maflist_dir, species_order) 
                        for gene_id, data in genes.items()]
            
            for result in pool.imap_unordered(process_gene, args_list):
                if result:
                    _, identity_dict, base_count_dict = result
                    id_writer.writerow(identity_dict)
                    bc_writer.writerow(base_count_dict)
    
    print(f"Results saved to:\n{identity_csv}\n{base_count_csv}")

if __name__ == '__main__':
    main()