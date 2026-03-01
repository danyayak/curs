FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for building some python packages)
# For this set of requirements, slim should be sufficient, but we might need gcc for some extensions if wheels aren't available.
# python-Levenshtein usually has wheels.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
