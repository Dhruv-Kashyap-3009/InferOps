FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY model ./model

# The trained model is not in git, so train it inside the image
RUN python model/train.py

# Render sets PORT at runtime; default 8000 keeps local runs simple
ENV PORT=8000
EXPOSE 8000

# Shell form is used so $PORT gets expanded at container start
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
