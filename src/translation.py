from transformers import MarianMTModel, MarianTokenizer
import torch

class Translator:
    def __init__(self):
        """
        Initializes the Translation Module.
        We load models lazily (only when needed) to save RAM.
        """
        self.models = {}
        self.tokenizers = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🔄 Translation Module initialized on {self.device}")

    def _get_model_name(self, src_lang):
        # 1. Get the first 2 letters (e.g., 'deu_Latn' -> 'de', 'spa_Latn' -> 'sp')
        short_code = src_lang[:2].lower() 
        
        # 2. Map standard codes to Hugging Face models
        mapping = {
            'de': 'Helsinki-NLP/opus-mt-de-en',
            'fr': 'Helsinki-NLP/opus-mt-fr-en',
            'es': 'Helsinki-NLP/opus-mt-es-en',
            'it': 'Helsinki-NLP/opus-mt-it-en',
            # FIX: Map 'sp' (from FastText) to 'es' (for Translation)
            'sp': 'Helsinki-NLP/opus-mt-es-en' 
        }
        
        return mapping.get(short_code)
        
        # Handle 3-letter codes from FastText (e.g., deu_Latn -> de)
        short_code = src_lang[:2].lower() 
        return mapping.get(short_code)

    def load_model(self, src_lang):
        """Loads the specific model for a language pair (e.g., German -> English)"""
        model_name = self._get_model_name(src_lang)
        if not model_name:
            print(f"⚠️ No translation model found for {src_lang}")
            return False

        if src_lang not in self.models:
            print(f"📥 Loading translation model for {src_lang}...")
            self.tokenizers[src_lang] = MarianTokenizer.from_pretrained(model_name)
            self.models[src_lang] = MarianMTModel.from_pretrained(model_name).to(self.device)
        
        return True

    def translate(self, text, src_lang):
        """
        Translates text from src_lang to English.
        """
        if not text or not isinstance(text, str):
            return text

        # Clean the language code (fasttext might give 'deu_Latn', we need 'de')
        clean_lang = src_lang[:2].lower()

        # If it's already English, don't touch it
        if clean_lang == 'en':
            return text

        # Ensure model is loaded
        if not self.load_model(clean_lang):
            return text  # Return original if we can't translate

        try:
            tokenizer = self.tokenizers[clean_lang]
            model = self.models[clean_lang]

            # Tokenize
            translated = model.generate(
                **tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)
            )
            
            # Decode
            result = tokenizer.decode(translated[0], skip_special_tokens=True)
            return result
            
        except Exception as e:
            print(f"❌ Translation failed: {e}")
            return text

# Quick Test
if __name__ == "__main__":
    translator = Translator()
    
    examples = [
        ("Das ist absolut schrecklich.", "de"),
        ("Me encanta este color, es perfecto.", "es"),
        ("C'est un peu cher pour la qualité.", "fr")
    ]
    
    print("\n🌍 Testing Translation:")
    for text, lang in examples:
        english_text = translator.translate(text, lang)
        print(f"[{lang}] {text} \n   ➡️  {english_text}")