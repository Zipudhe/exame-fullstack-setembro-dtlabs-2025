# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

WORKDIR /api

COPY requirements.txt  .

RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files for deployment
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

