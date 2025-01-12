##python 03.candidate-homologous-lncRNA.py 02.output-sheep-lncRNA-block.txt 02.output-deer-lncRNA-block.txt 01.output-sheep-deer-block.txt 03.output-sheep-deer-candidate-homolog.txt
##python 03.candidate-homologous-lncRNA.py 02.output-deer-lncRNA-block.txt 02.output-sheep-lncRNA-block.txt 01.output-sheep-deer-block.txt 03.output-deer-sheep-candidate-homolog.txt


import sys

def parse_IncRNA(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    block_to_location_dict = {}
    location_to_block_dict = {}
    location_and_block_to_num_dict = {}
    location_split_dict = {}
    for line in lines:
        strs = line.split()
        location = strs[0] + strs[1] + strs[2] + strs[3]
        block = strs[4] + strs[5] + strs[6]
        num = int(strs[7])
        if location_to_block_dict.get(location) is None:
            location_to_block_dict[location] = set()
        location_to_block_dict[location].add(block)
        if block_to_location_dict.get(block) is None:
            block_to_location_dict[block] = set()
        block_to_location_dict[block].add(location)
        location_and_block_to_num_dict[location + block] = num
        location_split_dict[location] = strs[0] + '\t' + strs[1] + '\t' + strs[2] + '\t' + strs[3]
    return location_to_block_dict, block_to_location_dict, location_and_block_to_num_dict, location_split_dict

def parse_mapfile(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    map_dict = {}
    for line in lines:
        strs = line.split()
        block1 = strs[0] + strs[1] + strs[2]
        block2 = strs[3] + strs[4] + strs[5]
        map_dict[block1] = block2
        map_dict[block2] = block1
    return map_dict

if __name__ == '__main__':
    import sys
    arg = sys.argv
    if len(arg) < 5:
        print('Usage: python 03.candidate-homologous-lncRNA.py <02.output-file-path1> <02.output-file-path2> <01.output-block-file-path> <03.output-file-path>')
        sys.exit(1)
    file1 = arg[1]
    file2 = arg[2]
    mapfile = arg[3]
    outputfile = arg[4]
    location_to_block_dict1, block_to_location_dict1, location_and_block_to_num_dict1, location_split_dict1 = parse_IncRNA(file1)
    location_to_block_dict2, block_to_location_dict2, location_and_block_to_num_dict2, location_split_dict2 = parse_IncRNA(file2)
    map_dict = parse_mapfile(mapfile)
    output = []
    for location1 in location_to_block_dict1.keys():
        blocks1 = location_to_block_dict1[location1]
        blocks2 = []
        for block in blocks1:
            blocks2.append(map_dict[block])

        location_to_block_dict_tmp = {}
        for block in blocks2:
            if block_to_location_dict2.get(block) is None:
                continue
            for location2 in block_to_location_dict2[block]:
                if location_to_block_dict_tmp.get(location2) is None:
                    location_to_block_dict_tmp[location2] = set()
                location_to_block_dict_tmp[location2].add(block)

        for location2 in location_to_block_dict_tmp.keys():
            block_num = 0
            for block in location_to_block_dict_tmp[location2]:
                block_num += location_and_block_to_num_dict2[location2 + block]
            total_num = 0
            for block in location_to_block_dict2[location2]:
                total_num += location_and_block_to_num_dict2[location2 + block]
            rate = block_num / total_num
            if rate > 0.4:
                rate = '%.5f' % rate
                output.append(location_split_dict1[location1] + '\t' + location_split_dict2[location2] + '\t' + rate)

    with open(outputfile, 'w') as f:  
        for line in output:
            f.write(line + '\n')

    print('Done')