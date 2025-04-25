FROM python:3.9-slim

# Set working directory
WORKDIR /app
# Copy project files
COPY server.py /app/
COPY requirements.txt /app/
COPY weights /app/weights/
COPY images /app/images/
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Expose port
EXPOSE 4000

# Run app
CMD ["gunicorn", "-b", "0.0.0.0:4000", "server:app"]
