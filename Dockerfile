FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for matplotlib and openpiv
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY app.py .

# Expose the port Hugging Face expects
EXPOSE 7860

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=7860

# Run the application
CMD ["python", "app.py"]
