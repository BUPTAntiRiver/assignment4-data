"""
A function that takes in a list of input file paths and performs fuzzy document deduplication
with minhash and LSH.
"""


import os
import unicodedata
import hashlib


def minhash_deduplication(
        input_files: list[os.PathLike],
        hash_num: int,
        band_num: int,
        n_gram_len: int,
        output_directory: os.PathLike,
        jaccard_threshold: float = 0.8
):
    """
    1. compute minhash signatures for all documents in input files
    2. use LSH with specified number of bands to identify candidate duplicate pairs
    3. compute the true ngram Jaccard similarity for candidate pairs and filter by threshold 0.8
    To improve recall, normalize documents by lowercasing, removing punctuation, normalizing whitespace,
    and removing accents, and applying NFD unicode normalization before computing.
    
    :param input_files: input file paths
    :type input_files: list[os.PathLike]
    :param hash_num: number of hash functions to use for computing minhash signatures
    :type hash_num: int
    :param band_num: number of bands to use for LSH
    :type band_num: int
    :param n_gram_len: length of n-grams for computing minhash signatures
    :type n_gram_len: int
    :param output_directory: directory to save deduplicated output files
    :type output_directory: os.PathLike
    """    

    signatures = {}
    for path in input_files:
        with open(path, encoding='utf-8') as f:
            # preprocess
            text = f.read()
            text = text.lower()
            text = ''.join(c for c in text if c.isalnum() or c.isspace())
            text = unicodedata.normalize('NFD', text)
            text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')

            # n-gram generation
            ngrams = set()
            tokens = text.split()
            for i in range(len(tokens) - n_gram_len + 1):
                ngram = ' '.join(tokens[i:i + n_gram_len])
                ngrams.add(ngram)
            
            # minhash signature computation
            signature = []
            for i in range(hash_num):
                hashes = [hash_func(ngram, i) for ngram in ngrams]
                signature.append(min(hashes))
            signatures[path] = signature

    # LSH to find candidate pairs
    bands = {}
    rows_per_band = hash_num // band_num
    for path, signature in signatures.items():
        for b in range(band_num):
            start = b * rows_per_band
            end = start + rows_per_band
            band_signature = tuple(signature[start:end])
            band_key = (b, band_signature)
            if band_key not in bands:
                bands[band_key] = []
            bands[band_key].append(path)
    candidate_pairs = set()
    for bucket in bands.values():
        if len(bucket) > 1:
            for i in range(len(bucket)):
                for j in range(i + 1, len(bucket)):
                    candidate_pairs.add((bucket[i], bucket[j]))

    # verify candidate pairs with Jaccard similarity
    duplicates = set()
    for path1, path2 in candidate_pairs:
        with open(path1, encoding='utf-8') as f1, open(path2, encoding='utf-8') as f2:
            text1 = f1.read()
            text2 = f2.read()
            ngrams1 = set()
            ngrams2 = set()
            tokens1 = text1.split()
            tokens2 = text2.split()
            for i in range(len(tokens1) - n_gram_len + 1):
                ngram = ' '.join(tokens1[i:i + n_gram_len])
                ngrams1.add(ngram)
            for i in range(len(tokens2) - n_gram_len + 1):
                ngram = ' '.join(tokens2[i:i + n_gram_len])
                ngrams2.add(ngram)
            intersection = len(ngrams1.intersection(ngrams2))
            union = len(ngrams1.union(ngrams2))
            jaccard_sim = intersection / union if union > 0 else 0
            if jaccard_sim >= jaccard_threshold:
                duplicates.add(path2)

    # output deduplicated files
    for path in input_files:
        filename = os.path.basename(path)
        output_path = os.path.join(output_directory, filename)
        if path in duplicates:
            continue
        with open(path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.write(f_in.read())


def hash_func(input, i: int) -> int:
    h1 = int(hashlib.md5(input.encode()).hexdigest(), 16)
    h2 = int(hashlib.sha1(input.encode()).hexdigest(), 16)
    return (h1 + i * h2) % (2**32 - 1)