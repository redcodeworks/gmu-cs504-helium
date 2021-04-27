
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from data import load_model


@st.cache(allow_output_mutation=True)
def load_tfidf():
    return load_model('lin_model_tfidf')


# %%
def view(**kwargs):

    lin_model_tfidf = load_tfidf()


    st.write("## Pitchfork Score Generator")

    text = st.text_area('Enter a review')

    if text:
        st.write("## Results")

        score = lin_model_tfidf.predict(pd.Series(text))[0]

        st.write("# " + str(round(score, 1)))

