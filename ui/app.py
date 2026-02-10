import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="PolyReview Intelligence",
    page_icon="🛍️",
    layout="wide"
)

# Title and Header
st.title("🛍️ PolyReview: Multilingual E-Commerce Intelligence")
st.markdown("""
**Goal:** Analyze customer reviews across multiple languages (🇬🇧 🇩🇪 🇫🇷 🇪🇸) to extract unified sentiment insights.
""")

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/processed_reviews.csv")
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filters")
    selected_lang = st.sidebar.multiselect(
        "Select Original Language",
        options=df['original_lang'].unique(),
        default=df['original_lang'].unique()
    )
    
    # Filter DataFrame
    filtered_df = df[df['original_lang'].isin(selected_lang)]

    # --- Top-Level Metrics ---
    total_reviews = len(filtered_df)
    positive_reviews = len(filtered_df[filtered_df['sentiment_label'] == 'POSITIVE'])
    negative_reviews = len(filtered_df[filtered_df['sentiment_label'] == 'NEGATIVE'])
    avg_positivity = (positive_reviews / total_reviews * 100) if total_reviews > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Reviews", total_reviews)
    col2.metric("Positive Feedback", f"{positive_reviews}")
    col3.metric("Positivity Rate", f"{avg_positivity:.1f}%")

    st.divider()

    # --- Charts Section ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🏆 Sentiment by Product")
        # Calculate positivity rate per product
        product_stats = filtered_df.groupby('product_id')['sentiment_label'].apply(
            lambda x: (x == 'POSITIVE').mean() * 100
        ).reset_index(name='Positivity Rate')
        
        fig_prod = px.bar(
            product_stats, x='product_id', y='Positivity Rate',
            color='Positivity Rate', range_y=[0, 100],
            title="Positivity Score per Product (0-100%)"
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    with c2:
        st.subheader("🌍 Language Distribution")
        lang_counts = filtered_df['original_lang'].value_counts().reset_index()
        lang_counts.columns = ['Language', 'Count']
        
        fig_lang = px.pie(
            lang_counts, values='Count', names='Language',
            title="Reviews by Language", hole=0.4
        )
        st.plotly_chart(fig_lang, use_container_width=True)

    # --- Raw Data View ---
    st.subheader("📝 Review Inspector")
    st.dataframe(filtered_df[['product_id', 'original_lang', 'text', 'translated_text', 'sentiment_label']])

else:
    st.error("❌ Data not found! Please run the pipeline first: `python -m src.pipeline`")