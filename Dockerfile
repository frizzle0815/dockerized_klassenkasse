# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5100

# Run the application
CMD ["python", "run.py"]