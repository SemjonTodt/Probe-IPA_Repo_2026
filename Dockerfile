FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ai_code_companion.py .

ENTRYPOINT ["python", "ai_code_companion.py"]
