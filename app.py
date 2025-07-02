import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
from fpdf import FPDF
import json
import nltk
import os

nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))

st.set_page_config(page_title="Emotional Tone Analyzer", layout="wide")

# --- Custom CSS for modern, neutral design ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*='css']  {
        font-family: 'Roboto', sans-serif;
    }
    .stApp {
        background: linear-gradient(120deg, #f0f4f8 0%, #d9e2ec 50%, #bcccdc 100%) !important;
    }
    .main-header {
        background: #234567;
        color: white;
        padding: 2rem 1rem 1.5rem 1rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 24px rgba(35,69,103,0.10);
        text-align: center;
    }
    .card {
        background: white;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        padding: 2rem 1.5rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: #234567;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        border: none;
        font-weight: 700;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: #19304d;
        color: #fff;
    }
    hr {
        border: none;
        border-top: 2px solid #e5e7eb;
        margin: 2rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar ---
st.sidebar.title("Emotional Tone Analyzer")
st.sidebar.markdown("""
Upload a text file (TXT or CSV) or paste your text below. The dashboard will analyze the emotional tone (sentiment) and visualize the results.
""")

uploaded_file = st.sidebar.file_uploader("Upload a text file (.txt or .csv)", type=["txt", "csv"])
text_input = st.sidebar.text_area("Or paste your text here:", height=150)
analyze = st.sidebar.button("Analyze")

# --- Main Header ---
st.markdown('<div class="main-header"><h1>Emotional Tone Analyzer Dashboard</h1><p>Analyze and visualize the emotional tone in your text data</p></div>', unsafe_allow_html=True)

texts = []
if uploaded_file is not None:
    if uploaded_file.name.endswith('.txt'):
        content = uploaded_file.read().decode('utf-8')
        texts = [line for line in content.splitlines() if line.strip()]
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        texts = df.iloc[:,0].dropna().astype(str).tolist()
elif text_input.strip():
    texts = [line for line in text_input.split('\n') if line.strip()]

if analyze and texts:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Sentiment Analysis Results")
    results = []
    for i, text in enumerate(texts):
        blob = TextBlob(text)
        try:
            polarity = float(blob.sentiment.polarity)
        except Exception:
            polarity = 0.0
        confidence = abs(polarity)
        try:
            key_phrases = ', '.join([str(phrase) for phrase in blob.noun_phrases])
        except Exception:
            key_phrases = str(blob.noun_phrases)
        if polarity > 0.1:
            sentiment = 'Positive'
            explanation = 'Polarity > 0.1: The text expresses positive sentiment.'
        elif polarity < -0.1:
            sentiment = 'Negative'
            explanation = 'Polarity < -0.1: The text expresses negative sentiment.'
        else:
            sentiment = 'Neutral'
            explanation = 'Polarity between -0.1 and 0.1: The text is neutral.'
        results.append({'Text': text, 'Polarity': polarity, 'Confidence': confidence, 'Sentiment': sentiment, 'Explanation': explanation, 'Key Phrases': key_phrases})
    results_df = pd.DataFrame(results)
    st.dataframe(results_df)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    # --- Visualization ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Visualizations")
    sentiment_counts = results_df['Sentiment'].value_counts()
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(2.5, 2.5))
        ax1.pie(sentiment_counts, labels=list(sentiment_counts.index.astype(str)), autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)
    with col2:
        fig2, ax2 = plt.subplots(figsize=(2.5, 2.5))
        sentiment_types = ['Negative', 'Neutral', 'Positive']
        sentiment_counts_sorted = sentiment_counts.reindex(sentiment_types, fill_value=0)
        y_values = [0 if s == 'Negative' else int(sentiment_counts_sorted[s]) for s in sentiment_types]
        ax2.plot(sentiment_types, y_values, marker='o', linestyle='-', color='blue')
        ax2.set_ylabel('Count')
        ax2.set_title('Sentiment Distribution (Line Graph)')
        st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    # --- Download Results ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Download Results")
    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name='sentiment_results.csv',
        mime='text/csv',
    )
    # JSON download
    json_data = results_df.to_json(orient='records', force_ascii=False, indent=2)
    if not isinstance(json_data, str):
        json_data = '[]'
    st.download_button(
        label="Download results as JSON",
        data=json_data,
        file_name='sentiment_results.json',
        mime='application/json',
    )
    # PDF download
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    pdf.cell(0, 8, "Sentiment Analysis Results", ln=True, align='C')
    col_names = list(results_df.columns)
    col_width = pdf.w / (len(col_names) + 1)
    # Header
    for col in col_names:
        pdf.cell(col_width, 8, col, border=1)
    pdf.ln()
    # Rows
    for i, row in results_df.iterrows():
        for col in col_names:
            cell = str(row[col])
            x_before = pdf.get_x()
            y_before = pdf.get_y()
            pdf.multi_cell(col_width, 8, cell, border=1, align='L')
            pdf.set_xy(x_before + col_width, y_before)
        pdf.ln(8)
    pdf_output = pdf.output(dest='S')
    if isinstance(pdf_output, str):
        pdf_bytes = pdf_output.encode('latin1')
    else:
        pdf_bytes = bytes(pdf_output)
    st.download_button(
        label="Download results as PDF",
        data=pdf_bytes,
        file_name='sentiment_results.pdf',
        mime='application/pdf',
    )
    st.markdown('</div>', unsafe_allow_html=True)
elif analyze and not texts:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.warning("Please upload a file or paste some text to analyze.")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.info("Please upload a file or paste some text, then click 'Analyze'.")
    st.markdown('</div>', unsafe_allow_html=True)

nltk.download('punkt', download_dir='nltk_data')
nltk.download('averaged_perceptron_tagger', download_dir='nltk_data')
nltk.download('brown', download_dir='nltk_data')
nltk.download('wordnet', download_dir='nltk_data')
nltk.download('maxent_treebank_pos_tagger', download_dir='nltk_data')
nltk.download('maxent_ne_chunker', download_dir='nltk_data')
nltk.download('words', download_dir='nltk_data') 