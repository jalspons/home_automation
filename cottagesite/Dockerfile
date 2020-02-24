# Set default image
FROM python:3.8-alpine

ENV DEBUG_VALUE "False"

# Add project files to the /usr/src/app
ADD . /usr/src/app

# Set default directory where CMD will execute
WORKDIR /usr/src/app

# Copy requirements.txt file to the current folder
COPY requirements.txt ./

# Install build deps
RUN apk add gcc musl-dev libffi-dev openssl-dev

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt
