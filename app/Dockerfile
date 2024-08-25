FROM python:3.10-slim

RUN useradd -m app

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN chown -R root:root /app
RUN chmod -R 667 /app

USER app
ENTRYPOINT ["python3", "app.py"]