FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
COPY . .
CMD  streamlit run app.py