"""
Detect harmful content in text data and returns a lable: "toxic" or "non-toxic with a confidence score.
"""

import fasttext
import os


def detect_nsfw(text: str) -> tuple[str, float]:
    model_path = os.path.join(os.path.dirname(__file__), "..", "data", "classifiers", "jigsaw_fasttext_bigrams_nsfw_final.bin")
    text = text.replace("\n", " ")
    model = fasttext.load_model(model_path)
    labels, scores = model.predict(text, k=1)
    label = labels[0].replace("__label__", "")
    score = scores[0]
    return label, score


def detect_hatespeech(text: str) -> tuple[str, float]:
    model_path = os.path.join(os.path.dirname(__file__), "..", "data", "classifiers", "jigsaw_fasttext_bigrams_hatespeech_final.bin")
    text = text.replace("\n", " ")
    model = fasttext.load_model(model_path)
    labels, scores = model.predict(text, k=1)
    label = labels[0].replace("__label__", "")
    score = scores[0]
    return label, score
