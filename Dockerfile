# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements
RUN pip install flask requests

# Make port 4001 available to the world outside this container
EXPOSE 4001

# Run app.py when the container launches
CMD ["python", "app.py"]
