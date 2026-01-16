"""
Implements a subset of Gopher quality filters.
    - Contain less than 50 or more than 100,000 words
    - Have a mean word length outside the range of 3 to 10 characters
    - Have more than 30% of lines ending with an ellipsis ("...")
    - contain less than 80% of words with at least one alphabetic character
"""


import nltk


def gopher_quality_filters(text):
    words = nltk.word_tokenize(text)
    lines = text.splitlines()

    num_words = len(words)
    if num_words < 50 or num_words > 100000:
        return False
    
    mean_word_length = sum(len(word) for word in words) / num_words
    if mean_word_length < 3 or mean_word_length > 10:
        return False
    
    ellipsis_lines = sum(1 for line in lines if line.strip().endswith("..."))
    if len(lines) > 0 and (ellipsis_lines / len(lines)) > 0.3:
        return False

    alphabetic_word_count = sum(1 for word in words if any(char.isalpha() for char in word))
    if num_words > 0 and (alphabetic_word_count / num_words) < 0.8:
        return False

    return True
