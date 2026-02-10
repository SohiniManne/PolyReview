import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class ReviewAnalytics:
    def __init__(self, data_path="data/processed_reviews.csv"):
        try:
            self.df = pd.read_csv(data_path)
            print("📊 Analytics Module Loaded Data")
        except FileNotFoundError:
            print("❌ Data file not found. Run pipeline first.")
            self.df = None

    def get_product_sentiment(self):
        """Calculates average sentiment per product"""
        if self.df is None: return None
        
        # Convert sentiment_label to numeric (POSITIVE=1, NEGATIVE=0)
        # This helps us calculate an 'Average Sentiment Score'
        self.df['numeric_sentiment'] = self.df['sentiment_label'].apply(
            lambda x: 1 if x == 'POSITIVE' else 0
        )
        
        # Group by Product ID
        stats = self.df.groupby('product_id').agg({
            'numeric_sentiment': 'mean', # % of positive reviews
            'id': 'count'
        }).reset_index()
        
        stats.columns = ['product_id', 'positivity_rate', 'review_count']
        stats['positivity_rate'] = (stats['positivity_rate'] * 100).round(1)
        
        return stats.sort_values(by='positivity_rate', ascending=False)

    def get_language_distribution(self):
        """Counts reviews per language"""
        if self.df is None: return None
        return self.df['original_lang'].value_counts().reset_index()

    def generate_report(self):
        """Prints a text summary of insights"""
        print("\n📈 --- BUSINESS INSIGHTS REPORT ---")
        
        # Product Performance
        print("\n🏆 Product Performance:")
        stats = self.get_product_sentiment()
        print(stats.to_string(index=False))
        
        best_product = stats.iloc[0]
        print(f"\n✅ WINNER: Product {int(best_product['product_id'])} with {best_product['positivity_rate']}% positive feedback.")

# Quick Test
if __name__ == "__main__":
    analytics = ReviewAnalytics()
    analytics.generate_report()