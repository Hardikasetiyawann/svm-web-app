import os
import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords

# =========================
# Load Kamus Slang
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KAMUS_PATH = os.path.join(BASE_DIR, "resources", "kamuskatabaku.xlsx")

kamus_slang = {}
if os.path.exists(KAMUS_PATH):
    kamus_df = pd.read_excel(KAMUS_PATH)
    kamus_df['tidak_baku'] = kamus_df['tidak_baku'].astype(str).str.lower()
    kamus_df['kata_baku'] = kamus_df['kata_baku'].astype(str).str.lower()
    kamus_slang = dict(zip(
        kamus_df['tidak_baku'],
        kamus_df['kata_baku']
    ))

# =========================
# Stopwords (Negasi Dipertahankan)
# =========================
stop_words = set(stopwords.words('indonesian'))
negation_words = {"tidak", "bukan", "jangan", "tak"}
stop_words = stop_words - negation_words

# =========================
# Stemmer
# =========================
stemmer = StemmerFactory().create_stemmer()

# =========================
# Regex Patterns
# =========================
URL_PATTERN = re.compile(r'http\S+|www\S+')
MENTION_PATTERN = re.compile(r'@\w+')
EMOJI_PATTERN = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
NON_ALPHA_PATTERN = re.compile(r'[^a-z\s]')
MULTISPACE_PATTERN = re.compile(r'\s+')

# =========================
# Preprocessing Function
# =========================
def preprocess_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # 1. Case folding
    text = text.lower()

    # 2. Remove URL & mention
    text = URL_PATTERN.sub(" ", text)
    text = MENTION_PATTERN.sub(" ", text)

    # 3. Remove emoji
    text = EMOJI_PATTERN.sub("", text)

    # 4. Remove numbers & symbols
    text = NON_ALPHA_PATTERN.sub(" ", text)

    # 5. Normalize whitespace
    text = MULTISPACE_PATTERN.sub(" ", text).strip()
    if not text:
        return ""

    # 6. Normalisasi slang
    words = [kamus_slang.get(w, w) for w in text.split()]
    if not words:
        return ""

    # 7. Stopword removal (negasi dipertahankan)
    words = [w for w in words if w not in stop_words]
    if not words:
        return ""

    # 8. Stemming
    stemmed_text = stemmer.stem(" ".join(words))

    # 9. Final filter: minimal 5 kata
    if len(stemmed_text.split()) < 3:
        return ""

    return stemmed_text
