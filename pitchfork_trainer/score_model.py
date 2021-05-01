#!/bin/python3
import joblib
import json, sys, os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from load_data import load_reviews
from sklearn.model_selection import cross_val_score 
import argparse


#  Excute with 'python3 score_model.py data/regression_1.joblib'
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Load Model')
    parser.add_argument('model', metavar='m', type=str,
                        help='joblib model to be scored')


    args = parser.parse_args()

    model = joblib.load(args.model)

    model_name = args.model.split('/')[-1]

    df = load_reviews()
        
    scores = cross_val_score(
        model,
        df["content"],
        df["score"],
        scoring="neg_root_mean_squared_error",
        cv=5,
    )

    avg_score = (sum(scores) / len(scores)) * -1

    with open(f"./data/{model_name}_score.txt", 'w') as f:
        f.write("Avg Score: {}\n".format(avg_score))
        f.write(str(scores))
        

    print("Avg Score: ", avg_score)
    print(scores)