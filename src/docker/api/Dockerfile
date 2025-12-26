# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY dataprojectv1 /app/dataprojectv1

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y vim
RUN apt-get clean
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
# ENV FLASK_APP=app.py

# Run the application
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]
# CMD ["python", "app.py"]
