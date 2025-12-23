import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "models")

def load_model(model_path: str):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model tidak ditemukan: {model_path}")
    return joblib.load(model_path)


TOPIC_DIR = os.path.join(MODEL_DIR, "topic")

tfidf_topic = load_model(os.path.join(TOPIC_DIR, "tfidf_topic.joblib"))
chi2_topic  = load_model(os.path.join(TOPIC_DIR, "chi2_topic.joblib"))
svm_topic   = load_model(os.path.join(TOPIC_DIR, "svm_topic.joblib"))

print("Model TOPIK berhasil dimuat")


SENTIMENT_DIR = os.path.join(MODEL_DIR, "sentiment")

tfidf_sentiment = load_model(os.path.join(SENTIMENT_DIR, "tfidf_sentiment.joblib"))
chi2_sentiment  = load_model(os.path.join(SENTIMENT_DIR, "chi2_sentiment.joblib"))
svm_sentiment   = load_model(os.path.join(SENTIMENT_DIR, "svm_sentiment.joblib"))

print("Model SENTIMEN berhasil dimuat")
