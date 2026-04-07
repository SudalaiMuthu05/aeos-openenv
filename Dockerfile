FROM python:3.10-slim

WORKDIR /app

# Copy all files
COPY . .

# Update pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port (HF uses 7860)
EXPOSE 7860

# Run server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
