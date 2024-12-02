#!/bin/python

input_file_path = 'niu-stringtie-merge-gffcompare.annotated.ixou.transcript.gtf'
output_file_path = 'niu-stringtie-merge-gffcompare.annotated.ixou.exon2.transcript.gtf'

def filter_gtf(input_file, output_file):
	transcript_exon_counts = {}
	transcript_lines = {}

	with open(input_file, 'r') as infile:
		for line in infile:
			if 'transcript_id "' in line:
				transcript_id = line.split('transcript_id "')[1].split('"')[0]
				transcript_exon_counts[transcript_id] = transcript_exon_counts.get(transcript_id, 0) + ('exon' in line)
				if transcript_id not in transcript_lines:
					transcript_lines[transcript_id] = []
				transcript_lines[transcript_id].append(line)

	with open(output_file, 'w') as outfile:
		for transcript_id, exon_count in transcript_exon_counts.items():
			if exon_count >= 2:
				outfile.writelines(transcript_lines[transcript_id])

filter_gtf(input_file_path, output_file_path)
