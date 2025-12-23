import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

def load_model(model_path: str, model_name: str):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"[ERROR] {model_name} tidak ditemukan: {model_path}")
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        raise RuntimeError(f"[ERROR] Gagal memuat {model_name}: {e}")

# =========================
# Load Model Topik
# =========================
TOPIC_DIR = os.path.join(MODEL_DIR, "topic")

tfidf_topic = load_model(
    os.path.join(TOPIC_DIR, "tfidf_topic.joblib"),
    "TF-IDF Topik"
)

chi2_topic = load_model(
    os.path.join(TOPIC_DIR, "chi2_topic.joblib"),
    "Chi-Square Topik"
)

svm_topic = load_model(
    os.path.join(TOPIC_DIR, "svm_topic.joblib"),
    "SVM Topik"
)

print("[INFO] Model Topik berhasil dimuat")

# =========================
# Load Model Sentimen
# =========================
SENTIMENT_DIR = os.path.join(MODEL_DIR, "sentiment")

tfidf_sentiment = load_model(
    os.path.join(SENTIMENT_DIR, "tfidf_sentiment.joblib"),
    "TF-IDF Sentimen"
)

chi2_sentiment = load_model(
    os.path.join(SENTIMENT_DIR, "chi2_sentiment.joblib"),
    "Chi-Square Sentimen"
)

svm_sentiment = load_model(
    os.path.join(SENTIMENT_DIR, "svm_sentiment.joblib"),
    "SVM Sentimen"
)

print("[INFO] Model Sentimen berhasil dimuat")
