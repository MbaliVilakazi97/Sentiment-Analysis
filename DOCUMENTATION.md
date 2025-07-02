# Emotional Tone Analyzer Documentation

## 1. Introduction
The Emotional Tone Analyzer is a modern web application built with Streamlit that enables users to analyze the emotional tone (sentiment) of text data. It is designed for educators, researchers, businesses, and anyone interested in understanding the sentiment behind written content. The app provides a user-friendly interface, insightful visualizations, and multiple export options.

## 2. Installation & Setup
To get started, clone the repository or download the source code. Install the required dependencies using:
```bash
pip install -r requirements.txt
```
Then, launch the app with:
```bash
streamlit run app.py
```
The app will automatically download necessary NLTK data and the DejaVuSans Unicode font for PDF export if they are not present.

## 3. Features & Usage
- **Data Input:** Upload `.txt` or `.csv` files, or paste text directly in the sidebar.
- **Sentiment Analysis:** The app uses TextBlob to classify each text as Positive, Neutral, or Negative, and extracts key phrases.
- **Visualizations:** Results are shown as a table, pie chart, and line graph for easy interpretation.
- **Export:** Download your results as CSV, JSON, or PDF (with Unicode support).

## 4. Technical Details
- **Backend:** Python, Streamlit, TextBlob, pandas, matplotlib, FPDF.
- **Unicode PDF Export:** The app uses DejaVuSans.ttf for full Unicode support in PDFs, downloading it if missing.
- **NLTK Data:** Required corpora are downloaded at runtime for robust noun phrase extraction.
- **Error Handling:** The app handles missing data, Unicode issues, and provides user feedback for common problems.

## 5. Troubleshooting & FAQ
- **Key phrases are missing:** Ensure your text contains nouns. The app downloads NLTK data automatically, but you may need to check your internet connection on first run.
- **PDF export fails:** The app will attempt to download the required font. If you see a 404 error, check the font URL in the code.
- **Unicode errors:** All exports use Unicode fonts, but if you see strange characters, ensure your input text is properly encoded.
- **Need more help?** Open an issue or contact the maintainer for support. 