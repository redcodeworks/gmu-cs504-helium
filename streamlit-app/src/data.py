# %%
import streamlit as st
import boto3
import io, os, json
import pandas as pd
import joblib
from pyathena import connect


def load_model(name):

    s3_key = f'{name}.joblib'

    with io.BytesIO() as f:
        boto3.client("s3").download_fileobj(Bucket=os.environ['model_bucket'], Key=s3_key, Fileobj=f)
        f.seek(0)
        model = joblib.load(f)

    return model


def _get_sql_query(name):

    with open(f'./sql/{name}.sql', 'r') as f:
        query = f.read()

    return query

def load_review_data():

    conn = connect(
        s3_staging_dir=os.environ['athena_result_bucket'],
        region_name=os.environ['aws_region'],
    )
    
    query = _get_sql_query('reviews')
    
    df = pd.read_sql_query(query, conn)

    return df

# %%
