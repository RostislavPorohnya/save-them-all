FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir --upgrade pip

CMD ["python", "main.py"]
