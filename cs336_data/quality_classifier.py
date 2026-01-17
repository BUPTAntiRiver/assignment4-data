"""
Train a quality classifier to filter out low-quality text data.

1. Scrape wikipedia external links into WARC format.
2. Downsample high-quality text data from scraped content with our previous filters.
3. Mark these as high-quality data, and common-crawl data as low-quality data.
4. Train a quality classifier with fastText, it should returns a numeric quality score (which is just the
probability of being high-quality).
"""


import fasttext

def label_quality(text: str) -> tuple[str, float]:
    model_path = "data/quality_classifier/quality.bin"
    text = text.replace("\n", " ")
    model = fasttext.load_model(model_path)
    labels, scores = model.predict(text, k=1)
    label = labels[0].replace("__label__", "")
    if label == "low":
        label = "cc"
    elif label == "high":
        label = "wiki"
    score = scores[0]
    return label, score