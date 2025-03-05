# Use official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY backend/services/cluster-service/app app/

# Expose the port FastAPI runs on
EXPOSE 8002

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]



## VOID

# # Use official Python image
# FROM python:3.11

# # Set the working directory inside the container
# WORKDIR /app

# # Copy requirements.txt first to leverage Docker cache
# COPY requirements.txt .
# COPY .env .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the application code into the container
# COPY ./services/cluster-service/app app/

# # Expose the port FastAPI runs on
# EXPOSE 8002

# # Run the application
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]