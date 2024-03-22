# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install build tools and dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev nginx



# Copy the current directory contents into the container at /app
COPY .. .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 for incoming HTTP traffic
EXPOSE 80

# Expose port 443 for incoming HTTPS traffic
EXPOSE 443

# Execute start.sh before starting Nginx
CMD gunicorn --bind 0.0.0.0:5000 apis:app
