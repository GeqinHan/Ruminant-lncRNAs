def process_file(input_path, output_path):
    """

    """
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            fields = line.strip().split('\t')
            if fields and float(fields[-1]) >= 50:
                outfile.write(line)

input_paths = [
    '02.input-sheep-lncRNA-block.txt',
    '02.input-deer-lncRNA-block.txt'
]
output_paths = [
    '02.output-sheep-lncRNA-block.txt',
    '02.output-deer-lncRNA-block.txt',
]

for input_path, output_path in zip(input_paths, output_paths):
    process_file(input_path, output_path)