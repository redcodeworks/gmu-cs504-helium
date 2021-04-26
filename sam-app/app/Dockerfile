FROM amazon/aws-lambda-python:3.8

COPY . ./

RUN python3.8 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
