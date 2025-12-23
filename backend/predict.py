from model_loader import (
    tfidf_topic,
    chi2_topic,
    svm_topic,
    tfidf_sentiment,
    chi2_sentiment,
    svm_sentiment
)

from preprocessing import preprocess_text


def predict_text(raw_text: str) -> dict:
    """
    Prediksi topik dan sentimen dari teks mentah
    """

    if raw_text is None or not isinstance(raw_text, str):
        return {
            "input": raw_text,
            "preprocessed": "",
            "kategori": "Tidak Diketahui",
            "sentimen": "Tidak Diketahui"
        }

    raw_text = raw_text.strip()
    if raw_text == "":
        return {
            "input": raw_text,
            "preprocessed": "",
            "kategori": "Tidak Diketahui",
            "sentimen": "Tidak Diketahui"
        }

   
    clean_text = preprocess_text(raw_text)

    if clean_text.strip() == "":
        return {
            "input": raw_text,
            "preprocessed": "",
            "kategori": "Tidak Diketahui",
            "sentimen": "Tidak Diketahui"
        }

   
    X_topic = tfidf_topic.transform([clean_text])
    X_topic = chi2_topic.transform(X_topic)
    topic_pred = svm_topic.predict(X_topic)[0]

   
    X_sent = tfidf_sentiment.transform([clean_text])
    X_sent = chi2_sentiment.transform(X_sent)
    sentiment_pred = svm_sentiment.predict(X_sent)[0]

    return {
        "input": raw_text,
        "preprocessed": clean_text,
        "kategori": str(topic_pred),
        "sentimen": str(sentiment_pred)
    }
