"""
Mask personally identifiable information (PII) in text data.
(a) email addresses -> |||EMAIL_ADDRESS|||
(b) phone numbers -> |||PHONE_NUMBER|||
(c) IP addresses -> |||IP_ADDRESS|||
"""


import re

def mask_email_addresses(text: str) -> tuple[str, int]:
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.sub(email_pattern, '|||EMAIL_ADDRESS|||', text), len(re.findall(email_pattern, text))


def mask_phone_numbers(text: str) -> tuple[str, int]:
    phone_pattern = r'(?:\+?(\d{1,3}))?[-.(]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})'
    return re.sub(phone_pattern, '|||PHONE_NUMBER|||', text), len(re.findall(phone_pattern, text))


def mask_ip_addresses(text: str) -> tuple[str, int]:
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    return re.sub(ip_pattern, '|||IP_ADDRESS|||', text), len(re.findall(ip_pattern, text))


def mask_pii(text: str) -> str:
    text, _ = mask_email_addresses(text)
    text, _ = mask_phone_numbers(text)
    text, _ = mask_ip_addresses(text)
    return text
