FROM python:3.8-slim

WORKDIR /function

COPY func.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["fdk", "/function/func.py", "handler"]
