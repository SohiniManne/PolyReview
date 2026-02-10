# 🛍️ PolyReview

### Multilingual E-Commerce Review Intelligence System

PolyReview is a **multilingual NLP system** that analyzes e-commerce product reviews written in different languages and generates **unified sentiment insights**.
The system detects the review language, translates it to English, and performs sentiment analysis to help businesses understand global customer feedback.

---

## 🚀 Features

* Automatic language detection
* Neural machine translation to English
* Transformer-based sentiment analysis
* Product-level sentiment aggregation
* Interactive local dashboard (Streamlit)
* Runs fully **locally** (no deployment required)

---

## 🧠 System Overview

1. User inputs a product review
2. Language of the review is detected
3. Review is translated to English
4. Sentiment is predicted (Positive / Neutral / Negative)
5. Insights are aggregated per product

---

## 🛠️ Tech Stack

* Python 3
* Hugging Face Transformers
* MarianMT (translation)
* mBERT / BERT (sentiment analysis)
* fastText / langdetect (language detection)
* Streamlit (UI)

---

## 📂 Project Structure

```text
ecommerce-nlp/
│
├── data/
│   └── reviews.csv
├── src/
│   ├── language_detection.py
│   ├── translation.py
│   ├── sentiment.py
│   ├── analytics.py
│   └── pipeline.py
├── ui/
│   └── app.py
├── config.yaml
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/polyreview.git
cd polyreview
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run ui/app.py
```

The dashboard will open in your browser for local testing.

---

## 📊 Example Output

* Detected Language: Spanish
* Translated Review: *“This product is amazing”*
* Sentiment: Positive (0.94)

---

## 📈 Evaluation Metrics

* Language detection accuracy
* Sentiment precision, recall, F1-score
* End-to-end pipeline latency

---

## 🎯 Use Cases

* Global e-commerce platforms
* Product feedback analysis
* Marketplace trust & quality monitoring

---

## 🔮 Future Enhancements

* Support for additional languages
* Fake review detection
* Real-time review streaming
* Model performance benchmarking across languages
* Cloud deployment (optional)

---

## 🎓 Academic Note

This project was developed for **educational and research purposes** to demonstrate applied NLP techniques in a real-world scenario.

---

## 📬 Contact

If you have suggestions or feedback, feel free to open an issue or reach out.
