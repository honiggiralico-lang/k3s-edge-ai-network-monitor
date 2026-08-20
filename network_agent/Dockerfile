FROM python:3.11-slim
WORKDIR /app
RUN pip install requests
COPY agent.py .
CMD ["python", "agent.py"]
