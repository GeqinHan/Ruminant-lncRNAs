import re

def process_line(line):
    parts = re.split(r'\s+', line.strip())
    
    parts[0] = parts[0].replace('deer.', '')
    
    parts[3] = parts[3].replace('sheep.', '')

    if int(parts[1]) > int(parts[2]):
        parts[1], parts[2] = parts[2], parts[1]
    
    if int(parts[4]) > int(parts[5]):
        parts[4], parts[5] = parts[5], parts[4]
    
    return '\t'.join(parts)

with open('01.input-sheep-deer-block.txt', 'r') as file_in, open('01.output-sheep-deer-block.txt', 'w') as file_out:
    for line in file_in:
        processed_line = process_line(line)
        file_out.write(processed_line + '\n')