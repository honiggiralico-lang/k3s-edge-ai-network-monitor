FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and the trained AI model
COPY app.py .
COPY network_anomaly_model.joblib .

# Expose the Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
