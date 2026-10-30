FROM python:3.11-slim

WORKDIR /app

COPY inventory.py .
COPY main.py .
COPY product.py .
COPY inventory.json .

CMD ["python", "main.py", "inventory.py", "product.py", "inventory.json"]