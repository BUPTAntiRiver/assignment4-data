import os


def exact_deduplication(paths: list[os.PathLike], output_dir: os.PathLike) -> None:
    """
    First build the set of all unique lines, then output the unique lines of input file to 
    corresponding output file. e.g. a/1.txt will be deduplicated and output to b/1.txt
    
    :param paths: a/1.txt, a/2.txt
    :type paths: list[os.PathLike]
    :param output_dir: b/
    :type output_dir: os.PathLike
    """

    # build the count of all lines
    line_counts = {}
    for path in paths:
        with open(path) as f:
            for line in f:
                key = hash(line)
                line_counts[key] = line_counts.get(key, 0) + 1
       
    # output only lines that appear exactly once across all files
    for path in paths:
        filename = os.path.basename(path)
        output_path = os.path.join(output_dir, filename)
        with open(path) as f_in, open(output_path, 'w') as f_out:
            for line in f_in:
                key = hash(line)
                if line_counts[key] == 1:
                    f_out.write(line)
