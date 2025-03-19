FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    wkhtmltopdf \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
