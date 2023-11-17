# Use the official Nginx image as the base image
FROM nginx:1.24

# Set an argument for the server's IP address
ARG SERVER_IP_ADDRESS

# Copy the shell script into the container
COPY setup.sh /usr/local/bin/

# Copy your configuration files and certificates into the container
COPY . /home/

# Make your script executable and run it
RUN chmod +x /usr/local/bin/setup.sh && /usr/local/bin/setup.sh

# Set the command or entry point
CMD ["nginx", "-g", "daemon off;"]
