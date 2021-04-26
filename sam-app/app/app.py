import json
from build_model import build_model

def lambda_handler(event, context):

    build_model()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "model built successfully!",
            }
        ),
    }
