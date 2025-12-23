from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

from predict import predict_text

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "OK",
        "service": "SVM Topic & Sentiment Classification API",
        "endpoints": {
            "/predict-text": "POST - analisis satu teks",
            "/predict-csv": "POST - analisis file CSV/Excel"
        }
    })


@app.route("/predict-text", methods=["POST"])
def predict_single():
    if not request.is_json:
        return jsonify({"error": "Request harus berupa JSON"}), 400

    data = request.get_json()
    text = data.get("text", "")

    result = predict_text(text)
    return jsonify(result), 200


@app.route("/predict-csv", methods=["POST"])
def predict_csv():
    if "file" not in request.files:
        return jsonify({"error": "File tidak ditemukan"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nama file kosong"}), 400

    # =========================
    # 1. Baca File
    # =========================
    ext = os.path.splitext(file.filename)[1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(file)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file)
        else:
            return jsonify({"error": "Format file harus .csv atau .xlsx"}), 400
    except Exception as e:
        return jsonify({"error": f"Gagal membaca file: {str(e)}"}), 400

    if df.empty:
        return jsonify({"error": "File kosong"}), 400

    # =========================
    # 2. Deteksi Kolom Teks
    # =========================
    TEXT_COLUMN_CANDIDATES = [
        "comment", "text", "content", "ulasan", "komentar",
        "full_text", "tweet", "pesan", "review", "isi"
    ]

    text_col = None
    for col in df.columns:
        if col.lower() in [c.lower() for c in TEXT_COLUMN_CANDIDATES]:
            text_col = col
            break

    if text_col is None:
        return jsonify({
            "error": "Kolom komentar tidak ditemukan.",
            "expected_columns": TEXT_COLUMN_CANDIDATES
        }), 400

    # =========================
    # 3. FILTER DATA KOSONG (INI KUNCI!)
    # =========================
    df = df[df[text_col].notna()]
    df = df[df[text_col].astype(str).str.strip() != ""]

    if df.empty:
        return jsonify({"error": "Semua baris komentar kosong"}), 400

    # =========================
    # 4. Prediksi Batch
    # =========================
    results = []

    for index, row in df.iterrows():
        raw_text = row[text_col]

        # 🔒 FILTER NAN & KOSONG SEBELUM predict
        if pd.isna(raw_text) or not isinstance(raw_text, str) or raw_text.strip() == "":
            continue   # LEWATI BARIS INI

        prediction = predict_text(raw_text)

        # Jika preprocessing menghasilkan kosong, skip
        if prediction.get("preprocessed", "").strip() == "":
            continue

        results.append({
            "text": raw_text,
            "preprocessed": prediction["preprocessed"],
            "kategori": prediction["kategori"],
            "sentimen": prediction["sentimen"]
        })


    if not results:
        return jsonify({"error": "Tidak ada data valid setelah preprocessing"}), 400

    return jsonify(results), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
