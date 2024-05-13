import streamlit as st
from streamlit_pages import scrapping, data_cleaning, predective_model, visualization, analyzing_sentiment


PAGES = {
    "Scrapping": scrapping.app,
    "Data Cleaning": data_cleaning.app,
    "Analyzing Sentiment": analyzing_sentiment.app,
    "Data Visualization": visualization.app,
    "Predective Model": predective_model.app
}

def main():
    
    st.title('🛰️ Crisis Forecast')
    st.write('By: Yousuf Ayman 202100476')

    st.header("📊 Project Oveview")
    st.write("""The aim of this project was to create a model for predecting receesion
            based on public sentiment by scrapping data from social media  websites 
            using tailored search filter and data analysis techniques to ensure 
            data integrity and accuracy.""")
    st.write('Please make sure all requirments are installed, use requirments.txt.')
    st.image("imgs/recession-markets-ben-Franklin-dollar-1-4-2.jpg")
    
    selection = st.selectbox("Choose a section to view:", list(PAGES.keys()))

    PAGES[selection]()

if __name__ == "__main__":
    main()
