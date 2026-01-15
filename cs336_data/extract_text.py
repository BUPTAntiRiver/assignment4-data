"""
Solution to problem extract_text
"""

from language_identification import identify_language
from fastwarc.warc import ArchiveIterator, WarcRecordType
from resiliparse.parse.encoding import detect_encoding
from resiliparse.extract.html2text import extract_plain_text


def extract_text(raw_html: bytes) -> str:
    encode_type = detect_encoding(raw_html)
    html = raw_html.decode(encode_type, errors="replace")
    plain_text = extract_plain_text(html)
    return plain_text


if __name__ == "__main__":
    WARC_FILE = "data/CC/example.warc.gz"
    WET_FILE = "data/CC/example.warc.wet.gz"
    identified_languages = []
    real_languages = []
    count = 20
    with open(WET_FILE, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type == WarcRecordType.conversion:
                raw_html = record.reader.read()
                text = extract_text(raw_html)
                language, score = identify_language(text)
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