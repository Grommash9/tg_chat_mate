
echo "SERVER_IP_ADDRESS: $SERVER_IP_ADDRESS"
# Update and install necessary packages
apt-get update && apt-get install -y openssl

# Create the necessary directories
mkdir -p /etc/nginx/snippets /etc/ssl/private /nginx-certs
mkdir -p /nginx-certs/$SERVER_IP_ADDRESS

if [[ $SERVER_IP_ADDRESS =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then

else
    apt-get update && apt-get install -y python3 
    apt-get install -y certbot python3-certbot-nginx
    certbot --nginx -d $SERVER_IP_ADDRESS --register-unsafely-without-email --agree-tos --no-eff-email
    cp /etc/letsencrypt/live/$SERVER_IP_ADDRESS/fullchain.pem /nginx-certs/$SERVER_IP_ADDRESS/fullchain.pem
    cp /etc/letsencrypt/live/$SERVER_IP_ADDRESS/privkey.pem /nginx-certs/$SERVER_IP_ADDRESS/privkey.pem
    cp /etc/letsencrypt/options-ssl-nginx.conf /nginx-certs/
    cp /etc/letsencrypt/ssl-dhparams.pem /nginx-certs/
    sed -i "s/SERVER_IP_PLACEHOLDER/$SERVER_IP_ADDRESS/g" /home/cert_bot_default.conf
    cp /home/cert_bot_default.conf /etc/nginx/conf.d/my-custom-server.conf
fi
