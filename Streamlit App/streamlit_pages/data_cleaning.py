import pandas as pd
import re
from langdetect import detect, LangDetectException
from datetime import datetime
import numpy as np
import os
from dateutil.relativedelta import relativedelta
import streamlit as st

def parseRelativeDates(text):
    current_time = datetime.now()
    units = {'m': 'minutes', 'h': 'hours', 'sec': 'seconds', 'd': 'days', 'w': 'weeks', 'y': 'years'}

    try:
        direct_date = pd.to_datetime(text)
        if pd.notna(direct_date):
            return direct_date
    except ValueError:
        pass
    match = re.match(r'(\d+)\s*([mhdwysec]+)', text)
    if match:
        amount, unit = match.groups()
        unit = units.get(unit.rstrip('s'), unit)
        kwargs = {unit: -int(amount)}
        calculated_date = current_time + relativedelta(**kwargs)
        return calculated_date
    else:
        return None

def normalizeText(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove user mentions
    text = re.sub(r'#\w+', '', text)  # Remove hashtags
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def languageDetection(text):
    try:
        return detect(text)
    except LangDetectException:
        return None


def app():
    st.header("🧹 Data Cleaning")
    st.image("imgs/illu_data_cleaning_blog_2-07.jpg")
    st.write("""
            Date Formatting and Sorting: 
                Standardize date formats using a custom function.
                Convert dates to a consistent datetime format.
                Sort data chronologically based on the date field. \n
            Text Normalization:
                Convert text to lowercase.
                Remove URLs, user mentions, hashtags, and special characters.
                Replace multiple spaces with a single space and trim whitespace. \n
            Handling Missing Data:
                Replace empty strings with NaN to unify missing data representation.
                Drop rows where the 'post' column is empty or NaN. \n
            Language Filtering:
                Detect the language of each post.
                Keep only posts written in English, discarding others.\n
            Duplicate Removal:
                Remove duplicate rows to ensure data uniqueness and relevance. \n

            """)

    datasetName = "datasets/training_scrapped_dataset.csv"
    currentDirectory = os.getcwd()
    datasetPath = os.path.join(currentDirectory, datasetName)
    data = pd.read_csv(datasetPath)

    st.subheader("Pre Cleaning")
    st.dataframe(data.head())

    if st.button("Clean Data"):
        # Correcting Date Formats
        data['date'] = data['date'].apply(lambda x: parseRelativeDates(x) if isinstance(x, str) else x)
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data.sort_values('date', inplace=True)

        # Normalizing Text
        data['post'] = data['post'].apply(normalizeText)

        # Replacing all empty strings with NaN
        data.replace('', np.nan, inplace=True)

        # Removing all rows with empty or "NaN" posts Columns
        data.dropna(subset=['post'], inplace=True)

        # Detecting languages and keeping posts only written in English
        data['language'] = data['post'].apply(languageDetection)
        data = data[data['language'] == 'en']

        # Removing Duplicate Rows & Columns
        data = data.drop_duplicates()

        st.subheader("Post Cleaning")
        st.dataframe(data.head())
