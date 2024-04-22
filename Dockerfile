# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir rembg flask gunicorn

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable
ENV SESSION_ID isnet-general-use

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
