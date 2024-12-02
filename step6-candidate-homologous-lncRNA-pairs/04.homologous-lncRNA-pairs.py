import sys

def main(file1, file2, output_file):
    lines_count = {}

    with open(file1, 'r') as f1:
        for line in f1:
            columns = line.strip().split('\t')
            key = '\t'.join(columns[:8]) 
            if key in lines_count:
                lines_count[key] += 1
            else:
                lines_count[key] = 1

    with open(file2, 'r') as f2:
        for line in f2:
            columns = line.strip().split('\t')
            swapped_columns = columns[4:8] + columns[:4]
            key = '\t'.join(swapped_columns)
            if key in lines_count:
                lines_count[key] += 1
            else:
                lines_count[key] = 1

    with open(output_file, 'w') as outfile:
        for line, count in lines_count.items():
            if count == 2:  
                outfile.write(line + '\n')

    print(f"Filtered data has been written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python 04.homologous-lncRNA-pairs.py <file1> <file2> <output_file>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]

    main(file1, file2, output_file)