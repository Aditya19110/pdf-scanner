FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app
COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p input output

CMD ["python", "main.py"]