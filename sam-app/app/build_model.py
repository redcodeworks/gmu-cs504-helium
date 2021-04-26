import numpy as np
import boto3, json, joblib, base64
import pandas as pd
from pyathena import connect
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

def build_model():
    client = boto3.client("athena")

    athena_result_bucket = "s3://cs504athena/"
    data_bucket =  "cs504tables"
    model_bucket = "cs504models"

    conn = connect(
    s3_staging_dir=athena_result_bucket,
    region_name="us-east-1",
    )
    
    query = """
        SELECT * FROM pitchfork.reviews r 
        JOIN pitchfork.content c
            ON r.reviewid = c.reviewid
    """
    
    df = pd.read_sql_query(query, conn)

    
    # reviews_path = 's3://{}/{}'.format(data_bucket, 'pitchfork/reviews/reviews.csv')
    # content_path = 's3://{}/{}'.format(data_bucket, 'pitchfork/content/content.csv')

    # df_reviews = pd.read_csv(reviews_path, sep='\t', index_col='reviewid')
    # df_content = pd.read_csv(content_path, sep='\t', index_col='reviewid')

    # df = df_reviews.join(df_content)

    lin_model_tfidf = Pipeline(
    [("tfidf", TfidfVectorizer(stop_words="english")), ("reg", LinearRegression())]
    )

    lin_model_tfidf.fit(df["content"].values.astype("U"), df["score"])

    with BytesIO() as f:
        joblib.dump(lin_model_tfidf, f)
        f.seek(0)
        boto3.client("s3").upload_fileobj(Bucket=model_bucket, Fileobj=f, Key='lin_model_tfidf.joblib')