# Use Python 3.9 to match project expectations
FROM python:3.9-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Workdir
WORKDIR /app

# System deps (for building some wheels like cryptography)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better layer caching)
COPY requirements.txt ./
# Clean out any leading lines that start with // (not valid for pip)
RUN grep -v '^//' requirements.txt > requirements.clean \
    && pip install --no-cache-dir -r requirements.clean \
    && rm requirements.clean

# Copy the rest of the application
COPY . .

# Expose the Flask port
EXPOSE 5500

# Run the app binding to 0.0.0.0 and ensure genesis block is added
# This imports your app module, adds the genesis block, and starts Flask
CMD ["python", "-c", "import app as m; m._blockchain.addGenesisBlock(); m.app.run(host='0.0.0.0', port=5500)"]
