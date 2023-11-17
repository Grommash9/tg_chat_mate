#!/bin/bash

# Use the provided SERVER_IP_ADDRESS
echo "SERVER_IP_ADDRESS: $SERVER_IP_ADDRESS"

# Update and install necessary packages
apt-get update && apt-get install -y openssl

# Create the necessary directories
mkdir -p /etc/nginx/snippets /etc/ssl/private /nginx-certs
mkdir -p /nginx-certs/$SERVER_IP_ADDRESS


if [[ $SERVER_IP_ADDRESS =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/C=US/ST=New York/L=New York/O=Bouncy Castles, Inc./OU=Ministry of Water/CN=${SERVER_IP_ADDRESS}/emailAddress=admin@your_domain.com"
    openssl dhparam -out /etc/nginx/dhparam.pem 2048

    # Replace placeholder with actual server IP
    sed -i "s/SERVER_IP_PLACEHOLDER/$SERVER_IP_ADDRESS/g" /home/default.conf

    # Move configuration files into place
    cp /home/self-signed.conf /etc/nginx/snippets/
    cp /home/ssl-params.conf /etc/nginx/snippets/
    cp /home/default.conf /etc/nginx/conf.d/my-custom-server.conf

    # Copy the certificates to a custom directory
    cp /etc/ssl/certs/nginx-selfsigned.crt /nginx-certs/
    cp /etc/ssl/private/nginx-selfsigned.key /nginx-certs/
else
    
fi
