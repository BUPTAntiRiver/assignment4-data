import fasttext
import os


def identify_language(text: str) -> tuple[str, float]:
    model_path = os.path.join(os.path.dirname(__file__), "..", "data", "classifiers", "lid.176.bin")
    model = fasttext.load_model(model_path)
    # fastText predict doesn't handle newlines, replace them with spaces
    text = text.replace("\n", " ")
    label, score = model.predict(text, k=1)
    language = label[0].replace("__label__", "")
    return language, score[0]
