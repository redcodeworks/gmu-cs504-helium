import joblib
import json, sys, os, argparse
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from load_data import load_reviews
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Specify a list of n-components')
    parser.add_argument('components', metavar='N', type=str, 
                        help='Format in comma delimited list e.g. 1,25,10,50')

    args = parser.parse_args()

    hyper_params = args.components.split(',')
    hyper_params = [ int(s) for s in hyper_params ]

    df = load_reviews()

    for i in hyper_params:

        model = Pipeline(
            [
                ("tfidf", TfidfVectorizer(stop_words="english")),
                ("lsa", TruncatedSVD(n_components=i, random_state=0)),
                ("reg", LinearRegression()),
            ]
        )

        model.fit(df["content"], df["score"])

        joblib.dump(model, f"./data/regression_{i}.joblib")
