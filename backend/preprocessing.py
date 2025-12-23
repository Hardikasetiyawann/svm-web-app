import os
import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KAMUS_PATH = os.path.join(BASE_DIR, "resources", "kamuskatabaku.xlsx") \
    if os.path.exists(os.path.join(BASE_DIR, "resources")) \
    else os.path.join(BASE_DIR, "kamuskatabaku.xlsx")

stopword_factory = StopWordRemoverFactory()
stop_words = set(stopword_factory.get_stop_words())

# Tambahan stopwords umum sosial media
CUSTOM_STOPWORDS = {
    "yg", "nya", "aja", "sih", "kok", "deh", "dong",
    "lah", "kan", "nih", "gak", "ga", "udah", "udah"
}
stop_words.update(CUSTOM_STOPWORDS)

stemmer = StemmerFactory().create_stemmer()

kamus_slang = {}

if os.path.exists(KAMUS_PATH):
    try:
        kamus_df = pd.read_excel(KAMUS_PATH)
        kamus_df['tidak_baku'] = kamus_df['tidak_baku'].astype(str).str.lower()
        kamus_df['kata_baku']  = kamus_df['kata_baku'].astype(str).str.lower()
        kamus_slang = dict(zip(
            kamus_df['tidak_baku'],
            kamus_df['kata_baku']
        ))
        print(f"Kamus slang dimuat: {len(kamus_slang)} kata")
    except Exception as e:
        print(f"[WARNING] Gagal memuat kamus slang: {e}")
else:
    print("[WARNING] File kamus slang tidak ditemukan, normalisasi dilewati.")

URL_PATTERN = re.compile(r'http\S+|www\S+')
MENTION_PATTERN = re.compile(r'@\w+')
NON_ALPHA_PATTERN = re.compile(r'[^a-z\s]')
MULTISPACE_PATTERN = re.compile(r'\s+')

def preprocess_text(text: str) -> str:
    """
    Membersihkan teks untuk keperluan klasifikasi topik & sentimen
    """

    if not isinstance(text, str):
        return ""

    # 1. Case folding
    text = text.lower()

    # 2. Hapus URL & mention
    text = URL_PATTERN.sub(" ", text)
    text = MENTION_PATTERN.sub(" ", text)

    # 3. Hapus emoji (unicode range)
    text = re.sub(
        "[\U00010000-\U0010ffff]",
        "",
        text
    )

    # 4. Hapus angka & simbol
    text = NON_ALPHA_PATTERN.sub(" ", text)

    # 5. Normalisasi spasi
    text = MULTISPACE_PATTERN.sub(" ", text).strip()

    if not text:
        return ""

    # 6. Normalisasi slang
    words = [kamus_slang.get(w, w) for w in text.split()]

    # 7. Stopword removal
    words = [w for w in words if w not in stop_words]

    if not words:
        return ""

    # 8. Stemming
    text = stemmer.stem(" ".join(words))

    return text
