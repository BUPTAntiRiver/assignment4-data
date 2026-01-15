"""
Solution to problem extract_text
"""


from fastwarc.warc import ArchiveIterator, WarcRecordType
from resiliparse.parse.encoding import detect_encoding
from resiliparse.extract.html2text import extract_plain_text


def extract_text(raw_html: bytes) -> str:
    encode_type = detect_encoding(raw_html)
    html = raw_html.decode(encode_type, errors="replace")
    plain_text = extract_plain_text(html)
    return plain_text


if __name__ == "__main__":
    import sys
    warc_path = sys.argv[1]
    output_count = 10
    with open(warc_path, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type == WarcRecordType.response:
                text = extract_text(record.reader.read())
                print(f"--- Extracted text from {record.record_id} ---")
                print(text)
                output_count -= 1
                if output_count == 0:
                    break