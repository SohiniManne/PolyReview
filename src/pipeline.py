import pandas as pd
from tqdm import tqdm
from src.language_detection import LanguageDetector
from src.translation import Translator
from src.sentiment import SentimentAnalyzer
import os

class ReviewPipeline:
    def __init__(self):
        print("🔧 Initializing PolyReview Pipeline...")
        self.lang_detector = LanguageDetector()
        self.translator = Translator()
        self.sentiment_analyzer = SentimentAnalyzer()
        print("✅ Pipeline Ready!")

    def process_review(self, text):
        """
        Runs a single review through the full AI stack.
        Returns: Dict with results
        """
        # 1. Detect Language
        lang, conf = self.lang_detector.detect_language(text)
        
        # 2. Translate if needed
        if lang != 'en':
            translated_text = self.translator.translate(text, lang)
        else:
            translated_text = text
            
        # 3. Analyze Sentiment (on the English text)
        sentiment = self.sentiment_analyzer.analyze(translated_text)
        
        return {
            'original_lang': lang,
            'lang_conf': conf,
            'translated_text': translated_text,
            'sentiment_label': sentiment['label'],
            'sentiment_score': sentiment['score']
        }

    def run(self, input_path="data/reviews.csv", output_path="data/processed_reviews.csv"):
        print(f"\n🚀 Starting processing on {input_path}...")
        
        # Load Data
        try:
            df = pd.read_csv(input_path)
        except FileNotFoundError:
            print("❌ Input file not found!")
            return

        # Create new columns
        tqdm.pandas() # Initialize progress bar for pandas
        
        results = []
        
        # Iterate with progress bar
        print(f"📊 Processing {len(df)} reviews...")
        for _, row in tqdm(df.iterrows(), total=len(df)):
            try:
                res = self.process_review(row['text'])
                results.append(res)
            except Exception as e:
                print(f"⚠️ Error processing row: {e}")
                results.append({
                    'original_lang': 'error',
                    'translated_text': row['text'],
                    'sentiment_label': 'neutral',
                    'sentiment_score': 0.0
                })

        # Combine results with original data
        results_df = pd.DataFrame(results)
        final_df = pd.concat([df, results_df], axis=1)
        
        # Save
        final_df.to_csv(output_path, index=False)
        print(f"\n✅ Done! Results saved to {output_path}")
        print(final_df[['text', 'original_lang', 'translated_text', 'sentiment_label']].head())

if __name__ == "__main__":
    pipeline = ReviewPipeline()
    pipeline.run()