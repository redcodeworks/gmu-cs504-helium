# %%
import boto3
from athena_helper import AthenaQuery
client = boto3.client('athena')

# %%
query = 'select * from reviews limit 10'
database = 'pitchfork'
athena_result_bucket = 's3://cs504athena/'

# %%

my_query = AthenaQuery(
    "SELECT * FROM reviews LIMIT 10",
    "pitchfork",
    athena_result_bucket
)

my_query.execute()
result_data = my_query.get_result()

# Process the result

result_data
# %%
