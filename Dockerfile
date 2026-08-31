# Optional — use if you need ffmpeg (AI video) on Render
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Render injects PORT
CMD ["python", "-m", "Manhwaflare.main"]
