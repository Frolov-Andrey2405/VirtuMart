# Base Python image
FROM python:3.9

# Set PYTHONUNBUFFERED environment variable to disable output buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . .

# Run the database migration command
RUN python manage.py migrate

# Command to start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
