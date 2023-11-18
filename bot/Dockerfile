# Use the official Python image with Python 3.11
FROM python:3.10
# Create a directory for your application
WORKDIR /home

# Copy your Pipfile and Pipfile.lock to the container
COPY . /home/

# Install pipenv
RUN pip install pipenv

# Install the dependencies using pipenv
RUN pipenv install --ignore-pipfile

# Expose the Nginx port
EXPOSE 2005

# Start your Telegram bot using pipenv
CMD pipenv run python -m support_bot
