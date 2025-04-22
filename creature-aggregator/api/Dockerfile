# api/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 1️⃣ Copy & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2️⃣ Create an 'api' folder and copy your code there
RUN mkdir api
COPY . api

# 3️⃣ Run via the 'api' package
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
