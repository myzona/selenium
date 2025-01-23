FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    wget gnupg unzip libnss3 libgconf-2-4 libxi6 libxrender1 xfonts-base xfonts-75dpi

# Install Chromium browser and ChromeDriver
RUN apt-get install -y chromium chromium-driver

# Install node-fetch globally
RUN npm install -g node-fetch

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app

# Start the application
CMD ["python", "app.py"]
