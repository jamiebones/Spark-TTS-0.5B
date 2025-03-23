FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libsndfile1 \
  git \
  ffmpeg \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Clone their official repo
RUN git clone https://github.com/SparkAudio/Spark-TTS.git /app/Spark-TTS

# Fix the requirements.txt file - correcting the numpy version
RUN sed -i 's/numpy==2.2.3/numpy==1.26.4/g' /app/Spark-TTS/requirements.txt

# Install dependencies from the fixed requirements.txt
WORKDIR /app/Spark-TTS
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Create the model directory
RUN mkdir -p pretrained_models/Spark-TTS-0.5B

# Copy the models into the expected directory structure
COPY models/Spark-TTS-0.5B pretrained_models/Spark-TTS-0.5B

# Create an inference script
COPY src/run_inference.py /app/run_inference.py

# Set the working directory back to /app
WORKDIR /app

# Set entrypoint
ENTRYPOINT ["python", "/app/run_inference.py"]
