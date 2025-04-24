#!/usr/bin/env python3

import os
import csv
import argparse
from collections import defaultdict
from intervaltree import IntervalTree
from multiprocessing import Pool, cpu_count

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate sequence identity between transcripts and other species.')
    parser.add_argument('input_gtf', help='Path to the input GTF file')
    parser.add_argument('input_maflist_dir', help='Directory containing MAFLIST files')
    parser.add_argument('output_dir', help='Directory to save output CSV files')
    return parser.parse_args()

def parse_gtf(gtf_file):
    transcripts = defaultdict(lambda: {'chrom': None, 'strand': None, 'exons': []})
    with open(gtf_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            if len(fields) < 9:
                continue
            if fields[2] != 'exon':
                continue

            chrom = fields[0]
            start = int(fields[3])
            end = int(fields[4])
            strand = fields[6]
            
            # Parse attributes to get transcript_id
            attributes = {}
            for attr in fields[8].split(';'):
                attr = attr.strip()
                if not attr:
                    continue
                key, value = attr.split(' ', 1)
                attributes[key] = value.strip('"')
            
            transcript_id = attributes.get('transcript_id') or attributes.get('transcript_id')
            if not transcript_id:
                continue

            if not transcripts[transcript_id]['chrom']:
                transcripts[transcript_id]['chrom'] = chrom
                transcripts[transcript_id]['strand'] = strand

            transcripts[transcript_id]['exons'].append({'start': start, 'end': end})

    return transcripts

def process_transcript(args):
    transcript_id, data, maflist_dir, species_order = args
    chrom = data['chrom']
    exons = data['exons']

    print(f"Processing transcript: {transcript_id}")

    maflist_filename = f"14sp.{chrom}.sheep_ref.hal2maf.maf.sort.maf.list"
    maflist_file = os.path.join(maflist_dir, maflist_filename)

    if not os.path.exists(maflist_file):
        print(f"Warning: MAFLIST file {maflist_file} does not exist.")
        return None

    exon_tree = IntervalTree()
    for exon in exons:
        start = exon['start']
        end = exon['end']
        exon_tree[start:end+1] = None

    species_match_counts = {species: 0 for species in species_order[1:]}  
    total_bases = 0

    try:
        with open(maflist_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            header = reader.fieldnames

            available_species = header[2:-1]  
            species_in_file = ['sheep'] + available_species

            species_map = {}
            for species in species_order[1:]:
                if species in species_in_file:
                    species_map[species] = species
                else:
                    print(f"Species {species} not found in MAFLIST file columns.")
                    species_map[species] = None  

            for row in reader:
                pos_str = row['pos']
                sheep_base = row['sheep']

                if sheep_base == '-':
                    continue

                try:
                    pos = int(pos_str)
                except ValueError:
                    continue 

                if exon_tree.overlaps(pos):
                    total_bases += 1
                    sheep_base = sheep_base.upper()
                    if sheep_base not in {'A', 'T', 'C', 'G'}:
                        continue
                    for species in species_order[1:]:
                        species_col = species_map.get(species)
                        if species_col and species_col in row:
                            species_base = row[species_col].upper()
                            if species_base == sheep_base and species_base in {'A', 'T', 'C', 'G'}:
                                species_match_counts[species] += 1
    except Exception as e:
        print(f"Error processing MAFLIST file {maflist_file}: {e}")
        return None

    if total_bases == 0:
        print(f"No valid bases found for transcript: {transcript_id}")
        return None

    identity_dict = {}
    base_count_dict = {}
    for species in species_order[1:]:  
        if species == 'sheep':
            identity_dict[species] = 1.0
            base_count_dict[species] = total_bases
        else:
            match_count = species_match_counts.get(species, 0)
            identity = match_count / total_bases if total_bases > 0 else 0
            identity_dict[species] = round(identity, 4)
            base_count_dict[species] = match_count

    print(f"Results for transcript {transcript_id}:")
    print(f"Identity: {identity_dict}")
    print(f"Base Count: {base_count_dict}")

    return transcript_id, identity_dict, base_count_dict

def main():
    args = parse_arguments()
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    species_order = ['Transcript_id', 'sheep', 'camel', 'pig', 'lesser_mouse_deer', 'pronghorn', 'giraffe',
                     'forest_musk_deer', 'cattle', 'goat', 'sika_deer', 'reindeer', 'hippo', 'killer_whale', 'tapir']

    transcripts = parse_gtf(args.input_gtf)

    identity_csv = os.path.join(args.output_dir, 'identity_results.csv')
    base_count_csv = os.path.join(args.output_dir, 'base_count_results.csv')

    with open(identity_csv, 'w', newline='') as id_csvfile, open(base_count_csv, 'w', newline='') as bc_csvfile:
        id_writer = csv.DictWriter(id_csvfile, fieldnames=species_order)
        bc_writer = csv.DictWriter(bc_csvfile, fieldnames=species_order)
        id_writer.writeheader()
        bc_writer.writeheader()

    args_list = [(transcript_id, data, args.input_maflist_dir, species_order) 
                for transcript_id, data in transcripts.items()]

    pool = Pool(processes=cpu_count())

    for result in pool.imap_unordered(process_transcript, args_list):
        if result is not None:
            transcript_id, identity_dict, base_count_dict = result

            identity_dict['Transcript_id'] = transcript_id
            base_count_dict['Transcript_id'] = transcript_id

            with open(identity_csv, 'a', newline='') as id_csvfile:
                id_writer = csv.DictWriter(id_csvfile, fieldnames=species_order)
                id_writer.writerow(identity_dict)

            with open(base_count_csv, 'a', newline='') as bc_csvfile:
                bc_writer = csv.DictWriter(bc_csvfile, fieldnames=species_order)
                bc_writer.writerow(base_count_dict)

    pool.close()
    pool.join()

    print(f"Results have been saved to:\n- {identity_csv}\n- {base_count_csv}")

if __name__ == '__main__':
    main()