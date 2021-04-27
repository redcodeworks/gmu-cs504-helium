# %%
import streamlit as st
import boto3
import io, os, json
import pandas as pd
import joblib


def load_model(name):

    s3_bucket = 'cs504models'
    s3_key = f'{name}.joblib'

    with io.BytesIO() as f:
        boto3.client("s3").download_fileobj(Bucket=s3_bucket, Key=s3_key, Fileobj=f)
        f.seek(0)
        model = joblib.load(f)

    return model



# %%
