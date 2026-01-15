"""
Solution to problem extract_text
"""


from resiliparse.parse.encoding import detect_encoding
from resiliparse.extract.html2text import extract_plain_text


def extract_text(raw_html: bytes) -> str:
    encode_type = detect_encoding(raw_html)
    html = raw_html.decode(encode_type, errors="replace")
    plain_text = extract_plain_text(html)
    return plain_text
