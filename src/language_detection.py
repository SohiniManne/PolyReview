import fasttext
from huggingface_hub import hf_hub_download
import os

class LanguageDetector:
    def __init__(self, model_name="lid.176.bin"):
        """
        Initialize the FastText language detection model.
        Downloads the model automatically if not present.
        """
        self.model_path = f"models/{model_name}"
        self._load_model()

    def _load_model(self):
        # Check if model exists locally, if not, download it
        if not os.path.exists(self.model_path):
            print(f"📥 Downloading FastText Language Model...")
            model_path = hf_hub_download(repo_id="facebook/fasttext-language-identification", filename="model.bin")
            # Move it to our models folder for structure
            os.rename(model_path, self.model_path)
        
        # Load the model (suppress warning regarding load_model)
        fasttext.FastText.eprint = lambda x: None
        self.model = fasttext.load_model(self.model_path)
        print("✅ Language Detection Model Loaded")

    def detect_language(self, text):
        """
        Detects language of a given text.
        Returns: (language_code, confidence_score)
        Example: ('en', 0.98)
        """
        if not text or not isinstance(text, str):
            return "unknown", 0.0
            
        # Remove newlines for fasttext
        clean_text = text.replace("\n", " ")
        
        # Predict (k=1 means return top 1 language)
        predictions = self.model.predict(clean_text, k=1)
        
        # Extract label and confidence
        # Format comes out like: (('__label__en',), array([0.98]))
        label = predictions[0][0]
        confidence = float(predictions[1][0])
        
        # Clean label (remove '__label__')
        lang_code = label.replace("__label__", "")
        
        return lang_code, confidence

# Quick Test (Run this file directly to test)
if __name__ == "__main__":
    detector = LanguageDetector()
    
    test_reviews = [
        "This product is amazing!",                 # English
        "Das ist absolut schrecklich.",             # German
        "Me encanta este color, es perfecto.",      # Spanish
        "C'est un peu cher pour la qualité."        # French
    ]
    
    print("\n🔎 Testing Language Detection:")
    for review in test_reviews:
        lang, conf = detector.detect_language(review)
        print(f"[{lang}] ({conf:.2f}): {review}")