import streamlit as st
from PyPDF2 import PdfReader
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import re

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to preprocess text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize the text
    words = word_tokenize(text)
    return words

# Streamlit app
st.title("PDF WordCloud Generator")
st.write("Upload a PDF file to extract text, preprocess it, and generate a WordCloud.")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Processing..."):
        # Extract text from PDF
        raw_text = extract_text_from_pdf(uploaded_file)
        
        # Preprocess text
        words = preprocess_text(raw_text)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word not in stop_words]

        # Generate WordCloud
        wordcloud = WordCloud(width=800, height=400, max_words=500, background_color='white').generate(' '.join(filtered_words))

        # Display the WordCloud
        st.subheader("WordCloud")
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # Display raw text (optional)
        if st.checkbox("Show Extracted Text"):
            st.subheader("Extracted Text")
            st.write(raw_text)
