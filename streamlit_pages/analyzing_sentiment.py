from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st
from joblib import load
import os

def sentimentAnalyzeVader(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

def sentimentAnalyzeTextBlob(text):
    negativeKeywords = ['unemployment', 'inflation', 'recession', 'interest rates', 'income inequality', "market crash", "poor", "unemployed", "homeless", "struggling", "high prices", "high mortgage", "lost house", "lost home", "move", "lost", "bankrupt"]
    blob = TextBlob(text)
    sentences = blob.sentences
    adjusted_sentiments = []
    
    for sentence in sentences:
        sentiment_score = sentence.sentiment.polarity
        if any(negKeyword.lower() in sentence.lower() for negKeyword in negativeKeywords):
            sentiment_score = min(sentiment_score, -0.2)
        elif -0.05 < sentiment_score < 0.05:
            sentiment_score = 0 
        adjusted_sentiments.append(sentiment_score)
    
    if not adjusted_sentiments:
        return 0
    
    return sum(adjusted_sentiments) / len(adjusted_sentiments)

def app(): 
    model = load("models/sentimentAnalyzerModel.joblib")
    revession_vectorizer = load("models/sentimentAnalyzerVectorizer.joblib")
    
    def sentimentAnalyzeReg(text):
        preprocessed_text = revession_vectorizer.transform([text])
        sentiment_score = model.predict(preprocessed_text)
        return sentiment_score[0]
    
    st.header("😡 Analyzing Sentiment")
    st.image("imgs/sentiment-analysis-2280x1160.png")
    st.write("""
                For analyzing sentiment, I tested several tools and libraries to find which of these tools would 
                provide the most accurate result. Of those tools I selected 2 to test TextBlob Sentiment Analyzer 
                and the Vader Sentiment Analyzer. Additionally I created a sentiment analyzing model using Sci-Kit 
                learn, and trained it on data retrieved from kaggle to test to see if more topic focused data would 
                help with analyzing sentiment. After Testing i decided to use the Vader sentiment analyzer as it was 
                the most accurate. Try them for yourself below. 
            """)
    st.subheader('Note')
    st.write("""Some models in the code have been pre-trained, and saved using joblib "dump" found in the 
             models folder which were then loaded using joblib "load". """)

    if st.checkbox('Show Custom Sentiment Analyzer Model Code:'):
            sentimentAnalyzerModelCode = """
            sentimentTrainingDataset= pd.read_csv("sentimentTrainerDataset.csv", encoding='ISO-8859-1')
            if sentimentTrainingDataset.empty:
                raise ValueError("Sentiment training dataset is empty.")

            requiredColumns = ['sentiment', 'text']
            if not set(requiredColumns).issubset(sentimentTrainingDataset.columns):
                raise ValueError("Required columns 'sentiment' and/or 'text' are missing in the dataset.")

            sentiment_mapping = {'negative': -1, 'neutral': 0, 'positive': 1}
            sentimentTrainingDataset['sentiment_score'] = sentimentTrainingDataset['sentiment'].map(sentiment_mapping)

            X_train, X_test, y_train, y_test = train_test_split(sentimentTrainingDataset['text'], sentimentTrainingDataset['sentiment_score'], test_size=0.2, random_state=42)

            vectorizer = TfidfVectorizer(max_features=60000)
            X_train_vectors = vectorizer.fit_transform(X_train)
            X_test_vectors = vectorizer.transform(X_test)

            model = RandomForestRegressor()
            model.fit(X_train_vectors, y_train)

            """
            st.code(sentimentAnalyzerModelCode, language='python')

    testSentence = st.text_input("Input a sentence to test the diffrent sentiment analyzers")
    if st.button("Generate Sentiment"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Vader: ", sentimentAnalyzeVader(testSentence))

        with col2:
            st.write(f"Text Blob: ", sentimentAnalyzeTextBlob(testSentence))
        
        with col3:
            st.write(f"Custom Model:", sentimentAnalyzeReg(testSentence))