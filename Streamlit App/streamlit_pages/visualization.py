import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import streamlit as st

def sentimentAnalyzeVader(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

def app():
    data = pd.read_csv('datasets/sentiment_data.csv')

    st.header("Visualizing Snetiment")
    st.subheader("Sentiment Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['sentiment_score'], bins=20, kde=True, ax=ax)
    ax.set_title('Distribution of Sentiment Scores')
    ax.set_xlabel('Sentiment Score')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Sentiment Over Time
    st.subheader("Sentiment Over Time")
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.lineplot(x='date', y='sentiment_score', data=data, ax=ax)
    ax.set_title('Sentiment Score Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment Score')
    st.pyplot(fig)  

    # Word Clouds
    st.subheader("Word Clouds")
    positiveTexts = data[data['sentiment_score'] > 0.1]
    negativeTexts = data[data['sentiment_score'] < 0.1]

    positiveString = ' '.join(positiveTexts['post'].tolist())
    negativeString = ' '.join(negativeTexts['post'].tolist())

    positiveWordCloud = WordCloud(background_color='white', max_words=200).generate(positiveString)
    negativeWordCloud = WordCloud(background_color='white', max_words=200).generate(negativeString)

    # Display Positive Word Cloud
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(positiveWordCloud, interpolation='bilinear')
    ax.axis('off')

    # Display Negative Word Cloud
    fig2, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(negativeWordCloud, interpolation='bilinear')
    ax.axis('off')

    col1, col2 = st.columns(2)
    with col1:
        st.header("Positive Word Cloud")
        st.pyplot(fig)

    with col2:
        st.header("Negative Word Cloud")
        st.pyplot(fig2)
