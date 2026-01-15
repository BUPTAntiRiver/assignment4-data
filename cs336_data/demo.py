from language_identification import identify_language
from extract_text import extract_text
from mask_pii import mask_pii
from fastwarc.warc import ArchiveIterator, WarcRecordType


def language_identification(WARC_FILE: str, WET_FILE: str, count: int):
    identified_languages = []
    real_languages = []
    with open(WARC_FILE, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type == WarcRecordType.response:
                raw_html = record.reader.read()
                text = extract_text(raw_html)
                language, _ = identify_language(text)
                identified_languages.append(language)
                count -= 1
                if count == 0:
                    break

    with open(WET_FILE, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type == WarcRecordType.conversion:
                lang = record.headers.get("WARC-Identified-Content-Language")
                real_languages.append(lang)
                count -= 1
                if count == 0:
                    break
    
    for identified, real in zip(identified_languages, real_languages):
        print(f"Identified: {identified}, Real: {real}")


def mask_pii_demo(WARC_FILE: str, WET_FILE: str, count: int):
    with open(WARC_FILE, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type == WarcRecordType.response:
                raw_html = record.reader.read()
                text = extract_text(raw_html)
                masked_text = mask_pii(text)
                print(masked_text[:100])
                count -= 1
                if count == 0:
                    break


if __name__ == "__main__":
    WARC_FILE = "data/CC/example.warc.gz"
    WET_FILE = "data/CC/example.warc.wet.gz"
    count = 20
    print("="*20)
    print("language identification demo\n")
    language_identification(WARC_FILE, WET_FILE, count)

    print("="*20)
    print("mask pii demo\n")
    mask_pii_demo(WARC_FILE, WET_FILE, count)