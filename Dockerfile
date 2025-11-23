# Use Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
# tesseract-ocr: for OCR
# poppler-utils: for pdf2image
# libpq-dev, gcc: for psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
# We set a dummy secret key for build step if needed, but usually handled by env vars
RUN python healthpredict/manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
# Adjust the path to wsgi application based on your project structure
CMD ["gunicorn", "--chdir", "healthpredict", "healthpredict.wsgi:application", "--bind", "0.0.0.0:8000"]