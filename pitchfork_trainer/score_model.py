#!/bin/python3
import joblib
import json, sys, os, glob
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from load_data import load_reviews
from sklearn.model_selection import cross_val_score
import argparse


def parse_files(argpaths):
    full_paths = [os.path.join(os.getcwd(), path) for path in args.path]

    files = set()

    for path in full_paths:
        if os.path.isfile(path):
            files.add(path)
        else:
            files |= set(glob.glob(path + "/*" + args.extension))

    return files


def score_model(file, df):
    model = joblib.load(file)

    model_name = file.split("/")[-1]

    scores = cross_val_score(
        model,
        df["content"],
        df["score"],
        scoring="neg_root_mean_squared_error",
        cv=5,
    )

    avg_score = (sum(scores) / len(scores)) * -1

    with open(f"./data/{model_name}_score.txt", "w") as f:
        f.write("Avg Score: {}\n".format(avg_score))
        f.write(str(scores))

    print("Avg Score: ", avg_score)
    print(scores)


#  Excute with 'python3 score_model.py data/regression_1.joblib'
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Load Model")
    parser.add_argument(
        "path", nargs="+", help="Model file path or a folder of model files."
    )
    parser.add_argument("-e", "--extension", default="", help="File extension filter")

    args = parser.parse_args()

    files = parse_files(args.path)

    df = load_reviews()

    [score_model(f, df) for f in files]
