FROM python:3.10

RUN apt-get update

# Install packages required to run the program.
RUN apt-get install -y build-essential
RUN apt-get install -y python3-pip poppler-utils
RUN apt-get update

# Copy and install requirements
COPY /app/requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY /app /app

# Set target directory as working directory.
WORKDIR /app

# Expose ports.
EXPOSE 80

# Startup server with Gunicorn binded to the specified host:port.
CMD [ "gunicorn", "-c", "gunicorn_config.py", "wsgi:app" ]
