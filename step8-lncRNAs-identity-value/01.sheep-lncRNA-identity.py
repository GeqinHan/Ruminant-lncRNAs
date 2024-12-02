import re
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

template_inputfile_gtf = "01.input-sheep-rumen-specific-high-expression-lncRNA.gtf"
template_inputdir_maflist = "~/maflist_ref_sheep/"
template_inputfile_species_list = "01.input-species-list"
output_identity_file = "01.output-identity.csv"
output_basecount_file = "01.output-base_matching_counts.csv"


with open(template_inputfile_species_list, 'r') as f:
    species_list = [line.strip() for line in f.readlines()]

transcripts = {}

max_workers = 10


with open(template_inputfile_gtf, 'r') as gtf:
    for line in gtf:
        if line.startswith("#"):
            continue

        fields = line.strip().split('\t')
        
        if fields[2] == "exon":
            chrom = fields[0]
            start = int(fields[3])
            end = int(fields[4])
            info = fields[8]

            match = re.search(r'transcript_id "([^"]+)"', info)
            if match:
                transcript_id = match.group(1)
                
                if transcript_id not in transcripts:
                    transcripts[transcript_id] = []
                
                transcripts[transcript_id].append((chrom, start, end))

def process_maflist(chrom, exon_start, exon_end):
    maf_file = f"{template_inputdir_maflist}14sp.chr{chrom}.sheep_ref.hal2maf.maf.sort.maf.list"
    base_matches = {species: 0 for species in species_list}
    total_bases = 0

    try:
        with open(maf_file, 'r') as maf:
            for line in maf:
                if line.startswith("chr"):  
                    continue
                
                fields = line.strip().split('\t')
                pos = fields[1]
                sheep_base = fields[2].upper()  
                
                if pos == "-" or sheep_base == "-":
                    continue

                pos = int(pos)
                if exon_start <= pos <= exon_end:
                    total_bases += 1  
                    for i, species in enumerate(species_list, 2):
                        species_base = fields[i].upper()  
                        if species_base == sheep_base and species_base != "X" and species_base != "-":
                            base_matches[species_list[i - 2]] += 1 
    except FileNotFoundError:
        print(f"The MAFLIST file was not found: {maf_file}")

    return base_matches, total_bases

threadpool = ThreadPoolExecutor(max_workers=max_workers)

with open(output_identity_file, 'w', newline='') as id_csv, open(output_basecount_file, 'w', newline='') as count_csv:
    identity_writer = csv.writer(id_csv)
    base_count_writer = csv.writer(count_csv)

    identity_writer.writerow(['transcript_id'] + species_list)
    base_count_writer.writerow(['transcript_id'] + species_list)

    for transcript_id, exons in transcripts.items():
        print(f"Processing transcript: {transcript_id}")
        species_total_matches = {species: 0 for species in species_list}
        overall_total_bases = 0 

        futures = []
        
        for exon in exons:
            chrom, exon_start, exon_end = exon
            future = threadpool.submit(process_maflist, chrom, exon_start, exon_end)
            futures.append(future)

        for future in as_completed(futures):
            base_matches, total_bases = future.result()

            for species in species_list:
                species_total_matches[species] += base_matches[species]
            overall_total_bases += total_bases

        identity_row = [transcript_id]
        base_count_row = [transcript_id]
        for species in species_list:
            if overall_total_bases > 0:
                identity = species_total_matches[species] / overall_total_bases
            else:
                identity = 0
            identity_row.append(f"{identity:.4f}")
            base_count_row.append(species_total_matches[species])
        
        identity_writer.writerow(identity_row)
        base_count_writer.writerow(base_count_row)
        print(f"Written to CSV - Transcript: {transcript_id}, Identity: {identity_row}, Base Count: {base_count_row}")

threadpool.shutdown()

print(f"Results written to {output_identity_file} and {output_basecount_file}")

