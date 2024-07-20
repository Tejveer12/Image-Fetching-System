# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

RUN apt update -y && apt install ffmpeg libxext6 libsm6 -y
# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the FastAPI application within the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
