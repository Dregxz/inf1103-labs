FROM python:3.11-slim

WORKDIR /app

COPY *.py products.csv inventory.json ./
COPY tests/ ./tests/

CMD ["python", "main.py"]
