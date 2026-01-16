from gopher_quality_filters import gopher_quality_filters
from language_identification import identify_language
from mask_pii import mask_email_addresses, mask_ip_addresses, mask_phone_numbers
from fastwarc.warc import ArchiveIterator, WarcRecordType
from harmful_content import detect_nsfw, detect_hatespeech


def fused_demo(WARC_FILE: str, WET_FILE: str, count: int):
    with open(WET_FILE, "rb") as f:
        for record in ArchiveIterator(f):
            if record.record_type == WarcRecordType.conversion:
                text = record.reader.read().decode('utf-8', errors='replace')
                language, _ = identify_language(text)
                if language != "en":
                    continue

                if not gopher_quality_filters(text):
                    continue
                
                nsfw_label, nsfw_score = detect_nsfw(text)
                hatespeech_label, hatespeech_score = detect_hatespeech(text)
                print(f"\nNSFW: {nsfw_label} ({nsfw_score:.2%}), Hatespeech: {hatespeech_label} ({hatespeech_score:.2%})")
                if nsfw_label == "toxic" or hatespeech_label == "toxic":
                    continue

                masked_text = mask_email_addresses(text)[0]
                masked_text = mask_phone_numbers(masked_text)[0]
                masked_text = mask_ip_addresses(masked_text)[0]

                print(masked_text[:500])

                count -= 1
                if count == 0:
                    break


if __name__ == "__main__":
    WARC_FILE = "data/CC/example.warc.gz"
    WET_FILE = "data/CC/example.warc.wet.gz"
    count = 20

    print("Fused Demo Running: only English, PII masked, NSFW and Hatespeech filtered\n")
    fused_demo(WARC_FILE, WET_FILE, count)