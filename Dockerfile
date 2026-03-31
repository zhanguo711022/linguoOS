FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY linguoos ./linguoos
COPY README.md ./README.md

EXPOSE 8000

CMD ["uvicorn", "linguoos.main:app", "--host", "0.0.0.0", "--port", "8000"]
