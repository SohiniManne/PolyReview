from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        """
        Initializes the Sentiment Analysis model.
        We use DistilBERT finetuned on SST-2 (standard benchmark).
        """
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        print(f"🧠 Loading Sentiment Model ({model_name})...")
        
        # The pipeline handles tokenization and prediction automatically
        self.analyzer = pipeline("sentiment-analysis", model=model_name)

    def analyze(self, text):
        """
        Analyzes sentiment of English text.
        Returns: {'label': 'POSITIVE'/'NEGATIVE', 'score': 0.99}
        """
        if not text:
            return {'label': 'NEUTRAL', 'score': 0.0}
            
        try:
            # The model has a max length of 512 tokens. 
            # We truncate to 512 to prevent errors on long reviews.
            result = self.analyzer(text, truncation=True, max_length=512)
            
            # Result looks like: [{'label': 'POSITIVE', 'score': 0.99}]
            return result[0]
            
        except Exception as e:
            print(f"❌ Sentiment analysis failed: {e}")
            return {'label': 'ERROR', 'score': 0.0}

# Quick Test
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    examples = [
        "I love this product! It's amazing.",        # Clear Positive
        "This is garbage. Don't buy it.",            # Clear Negative
        "It's okay, not the best but works.",        # Mixed/Neutralish (Model might force POS/NEG)
        "The delivery was slow but the item is good." # Conflicting signals
    ]
    
    print("\n🧠 Testing Sentiment Analysis:")
    for text in examples:
        sentiment = analyzer.analyze(text)
        print(f"Text: {text}")
        print(f"Result: {sentiment['label']} ({sentiment['score']:.4f})\n")