from unicodedata import normalize
import re

def normalize_text(text: str):
    text = text.lower()
    text = normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s]', '', text)
    text = text.split()
    text = ' '.join(text)

    return text