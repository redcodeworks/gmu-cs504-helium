import joblib
import json, sys, os, argparse
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from load_data import load_reviews
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Specify a list of n-estimators')
    parser.add_argument('estimators', metavar='N', type=str, 
                        help='Format in comma delimited list e.g. 1,25,10,50')

    args = parser.parse_args()

    hyper_params = args.estimators.split(',')
    hyper_params = [ int(s) for s in hyper_params ]

    df = load_reviews()

    for i in hyper_params:

        model = Pipeline(
            [
                ("tfidf", TfidfVectorizer(stop_words="english")),
                ("forest", RandomForestRegressor(n_estimators=i, random_state=0)),
            ]
        )

        model.fit(df["content"], df["score"])

        joblib.dump(model, f"./data/random_forest_{i}.joblib", compres=3)
