FFROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose application port
EXPOSE 7860

# Start Flask app via Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:super_kart_predictor_api"]
