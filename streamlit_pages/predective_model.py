from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from joblib import load
import streamlit as st
import numpy as np
import os


def app():
    ######Preparing for model testing
    processedDF = pd.read_csv('datasets/sentiment_data.csv')
    
    processedDF['date'] = pd.to_datetime(processedDF['date'])
    
    startDate = pd.to_datetime('2007-12-01')
    endDate = pd.to_datetime('2009-01-01')

    processedDF['recession'] = processedDF['date'].apply(lambda x: startDate <= x <= endDate)

    X = processedDF[['sentiment_score']] 
    y = processedDF['recession']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    predictRecessionModel = RandomForestClassifier()
    predictRecessionModel.fit(X_train, y_train)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    def calculateRecessionProbability(df):
        X_new = df[['sentiment_score']]

        predictedRecession = predictRecessionModel.predict_proba(X_new)[:, 1]

        recessionProbability = np.mean(predictedRecession)
        
        return recessionProbability

    #################################
    
    st.header("Predictive Model")
    st.image('imgs/predective_modeling.png')
    st.write("""
             The model was trained using the RandomForestClassifier; which creates a cluster of decision trees 
             using random subsets of data and features. It improves prediction accuracy by averaging the 
             results from all trees, effectively reducing overfitting and increasing robustness against 
             noise in the dataset.
             """)
    
    
    st.subheader("Testing Model Accuracy")
    
    predictions = predictRecessionModel.predict(X_test)
    modelAccuracy = accuracy_score(y_test, predictions)
    st.write(f"Model Accuracy: {modelAccuracy}")
    
    if st.checkbox('Show Code For Model:'):
        sentimentAnalyzerModelCode = """
            X = data[['sentiment_score']] 
            y = data['recession']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            predictRecessionModel = RandomForestClassifier()
            predictRecessionModel.fit(X_train, y_train)
            
            #####################################################
            
            def calculateRecessionProbability(df):
                X_new = df[['sentiment_score']]

                predictedRecession = predictRecessionModel.predict_proba(X_new)[:, 1]

                recessionProbability = np.mean(predictedRecession)
                
                return recessionProbability
        """
        st.code(sentimentAnalyzerModelCode, language='python')
    
    # Model implementation
    new_data = pd.read_csv("datasets/testing_sentiment_analysis.csv", encoding='ISO-8859-1') 

    st.subheader("Scrapped Dataset from April 2024 for testing Model")
    st.dataframe(new_data.head())

    recessionProbability = calculateRecessionProbability(new_data)

    st.write(f"Overall probability of recession: {recessionProbability}")