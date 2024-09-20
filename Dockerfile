FROM python:3.12

ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install Poppler and dependencies
RUN apt-get update && \
    apt-get install -y \
    poppler-utils \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . /app/

# Expose port (if needed, e.g., for Django development server)
EXPOSE 8000

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
