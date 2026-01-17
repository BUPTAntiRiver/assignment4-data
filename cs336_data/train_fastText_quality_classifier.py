"""
Train utils.
"""


from fastwarc.warc import ArchiveIterator, WarcRecordType
from gopher_quality_filters import gopher_quality_filters
from language_identification import identify_language
from mask_pii import mask_email_addresses, mask_ip_addresses, mask_phone_numbers
from harmful_content import detect_nsfw, detect_hatespeech
from extract_text import extract_text
import tqdm
import random


def build_dataset(positive_path, negative_path, output_path):
    """
    Extract positive samples that are truly high-quality (pass our filters)
    each data point is a line of text with "__label__high" or "__label__low" prefix.
    
    :param positive_path: warc.gz file, raw WARC data containing high-quality text data.
    :param negative_path: warc.gz file, raw WARC data containing low-quality text data.
    :param output_path: Path to save the processed dataset of txt format.
    """

    # get positive samples
    positive_samples = []
    with open(positive_path, "rb") as f:
        for record in tqdm.tqdm(ArchiveIterator(f)):
            if record.record_type == WarcRecordType.response:
                text = extract_text(record.reader.read())
                language, _ = identify_language(text)
                if language != "en":
                    continue
                if not gopher_quality_filters(text):
                    continue
                nsfw_label, _ = detect_nsfw(text)
                hatespeech_label, _ = detect_hatespeech(text)
                if nsfw_label == "toxic" or hatespeech_label == "toxic":
                    continue
                masked_text = mask_email_addresses(text)[0]
                masked_text = mask_phone_numbers(masked_text)[0]
                masked_text = mask_ip_addresses(masked_text)[0]
                masked_text = masked_text.replace("\n", " ").strip()
                if len(masked_text) > 0:
                    positive_samples.append(f"__label__high {masked_text}\n")

    # get negative samples same amout as positive samples
    negative_samples = []
    with open(negative_path, "rb") as f:
        for record in tqdm.tqdm(ArchiveIterator(f)):
            if record.record_type == WarcRecordType.response:
                text = extract_text(record.reader.read())
                masked_text = mask_email_addresses(text)[0]
                masked_text = mask_phone_numbers(masked_text)[0]
                masked_text = mask_ip_addresses(masked_text)[0]
                masked_text = masked_text.replace("\n", " ").strip()
                if len(masked_text) > 0:
                    negative_samples.append(f"__label__low {masked_text}\n")
                if len(negative_samples) >= len(positive_samples):
                    break
    
    # save dataset
    with open(output_path, "w", encoding="utf-8") as f:
        all_samples = positive_samples + negative_samples
        random.shuffle(all_samples)
        f.writelines(all_samples)


if __name__ == "__main__":
    POSITIVE_WARC = "data/wiki/subsampled_positive_urls.warc.gz"
    NEGATIVE_WARC = "data/CC/example.warc.gz"
    OUTPUT_PATH = "data/quality_classifier/quality_dataset.txt"

    print("Building quality classifier dataset...")
    build_dataset(POSITIVE_WARC, NEGATIVE_WARC, OUTPUT_PATH)
    print(f"Dataset saved to {OUTPUT_PATH}")