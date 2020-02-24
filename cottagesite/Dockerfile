# Set default image
FROM python:alpine

# Add project files to the /usr/src/app
ADD . /usr/src/app

# Set default directory where CMD will execute
WORKDIR /usr/src/app

# Copy requirements.txt file to the current folder
COPY requirements.txt ./

# Install build deps
RUN apk update
RUN apk add gcc musl-dev libffi-dev openssl-dev

# Install project dependencies
RUN pip install -U pip
RUN pip install --no-cache-dir -Ur requirements.txt

# Collect static media
RUN ls -laR
RUN python manage.py collectstatic --noinput