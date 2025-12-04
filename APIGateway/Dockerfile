FROM python:3.11-slim

# Prevent python from writing pyc files to disc and buffering stdout
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

EXPOSE 5001
CMD ["python", "app.py"]
