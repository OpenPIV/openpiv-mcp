FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for matplotlib, openpiv, and gradio
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY gradio_app.py .
COPY src/ ./src/

# Add src to Python path for openpiv_mcp imports
ENV PYTHONPATH=/app/src

# Expose the port Hugging Face expects
EXPOSE 7860

# Set environment variables
ENV PORT=7860
ENV HOST=0.0.0.0

# Run the Gradio application with MCP server
CMD ["python", "gradio_app.py"]
