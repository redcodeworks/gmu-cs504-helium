import pandas as pd
from pyathena import connect
import os, boto3

def load_reviews():
    conn = connect(
        s3_staging_dir="s3://cs504athena/",
        region_name="us-east-1",
    )

    query = """
        SELECT * FROM "pitchfork-etl".reviews r
        JOIN "pitchfork-etl".content c
            ON r.reviewid = c.reviewid
        WHERE r.author IN (
        SELECT expert_desc FROM "pitchfork-etl".experts
        );
    """

    df = pd.read_sql(query, conn)

    df.to_csv("./data/pitchfork_reviews.csv")

    return df
