# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install the required dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script and the model file to the container's working directory
COPY attiredetectionmodel.h5 /app/
COPY app.py /app/

# Expose the port that Flask will be running on
EXPOSE 5000

# Start the Flask app when the container starts
CMD ["python", "app.py"]
