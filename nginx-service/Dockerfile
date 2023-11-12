# Use the official Nginx image as the base image
FROM nginx:1.24

ARG SERVER_IP_ADDRESS
RUN echo "SERVER_IP_ADDRESS: $SERVER_IP_ADDRESS"

RUN apt-get update && apt-get install -y nginx openssl

# Create the necessary directories
RUN mkdir -p /etc/nginx/snippets /etc/ssl/private

# Generate self-signed SSL certificate and other configurations
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/C=US/ST=New York/L=New York/O=Bouncy Castles, Inc./OU=Ministry of Water/CN=${SERVER_IP_ADDRESS}/emailAddress=admin@your_domain.com" && openssl dhparam -out /etc/nginx/dhparam.pem 2048 && rm -rf /etc/nginx/conf.d/default.conf

COPY . /home/

RUN touch /etc/nginx/snippets/self-signed.conf
RUN touch /etc/nginx/snippets/ssl-params.conf
RUN sed -i "s/SERVER_IP_PLACEHOLDER/$SERVER_IP_ADDRESS/g" /home/default.conf

RUN cat home/self-signed.conf > /etc/nginx/snippets/self-signed.conf
RUN cat home/ssl-params.conf > /etc/nginx/snippets/ssl-params.conf
RUN cat home/default.conf > /etc/nginx/conf.d/my-custom-server.conf

RUN mkdir -p /nginx-certs

RUN touch /nginx-certs/nginx-selfsigned.crt
RUN cat /etc/ssl/certs/nginx-selfsigned.crt > /nginx-certs/nginx-selfsigned.crt
RUN touch /nginx-certs/nginx-selfsigned.key
RUN cat /etc/ssl/private/nginx-selfsigned.key > /nginx-certs/nginx-selfsigned.key

# Set the command or entry point
CMD ["nginx", "-g", "daemon off;"]