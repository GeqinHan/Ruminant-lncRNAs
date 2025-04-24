#!/bin/python

transcript_ids_file = 'species-gffcompare.annotated.ixou.transcript.ID'
input_gtf_file = 'species-gffcompare.annotated.gtf'
output_gtf_file_step1 = 'species-gffcompare.annotated.ixou.transcript.gtf'

def save_matching_transcripts(transcript_ids_file, input_gtf_file, output_gtf_file_step1):
    with open(transcript_ids_file, 'r') as f:
        transcript_ids = {line.strip() for line in f}

    matched_lines = []

    with open(input_gtf_file, 'r') as infile:
        for line in infile:
            for tid in transcript_ids:
                if tid in line:  
                    matched_lines.append(line)
                    break 

    with open(output_gtf_file_step1, 'w') as outfile:
        outfile.writelines(matched_lines)

save_matching_transcripts(transcript_ids_file, input_gtf_file, output_gtf_file_step1)
