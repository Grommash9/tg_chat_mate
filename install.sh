sudo DEBIAN_FRONTEND=noninteractive apt update
sudo DEBIAN_FRONTEND=noninteractive apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu focal stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo DEBIAN_FRONTEND=noninteractive apt update
sudo DEBIAN_FRONTEND=noninteractive apt install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
sudo docker --version
sudo docker run hello-world
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

echo "Docker and Docker Compose have been installed successfully."

docker compose up -d

set -a
source .env
set +a

echo "DOMAIN: $DOMAIN"


if [[ "$ISSUE_SSL" == "true" ]]; then
    if [[ $DOMAIN =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        docker exec tg_chat_mate-nginx-service-1 /bin/bash -c "\
        apt-get update && apt-get install -y openssl && \
        mkdir -p /nginx-certs/$DOMAIN && \
        mkdir -p /etc/nginx/snippets /etc/ssl/private /nginx-certs && \
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj \"/C=US/ST=New York/L=New York/O=Bouncy Castles, Inc./OU=Ministry of Water/CN=\$DOMAIN/emailAddress=admin@your_domain.com\" && \
        openssl dhparam -out /etc/nginx/dhparam.pem 2048 && \
        sed -i \"s/SERVER_IP_PLACEHOLDER/\$DOMAIN/g\" /home/default.conf && \
        cp /home/self-signed.conf /etc/nginx/snippets/ && \
        cp /home/ssl-params.conf /etc/nginx/snippets/ && \
        cp /home/default.conf /etc/nginx/conf.d/my-custom-server.conf && \
        cp /etc/ssl/certs/nginx-selfsigned.crt /nginx-certs/ && \
        cp /etc/ssl/private/nginx-selfsigned.key /nginx-certs/"
    else
        docker exec tg_chat_mate-nginx-service-1 /bin/bash -c "apt-get update && apt-get install -y python3 && \
        apt-get install -y certbot python3-certbot-nginx && \
        sed -i \"s/SERVER_IP_PLACEHOLDER/$DOMAIN/g\" /home/cert_bot_base.conf && \
        sed -i \"s/SERVER_IP_PLACEHOLDER/$DOMAIN/g\" /home/cert_bot_default.conf && \
        cp /home/cert_bot_base.conf /etc/nginx/conf.d/default.conf && \
        certbot --nginx -d $DOMAIN --register-unsafely-without-email --agree-tos --no-eff-email --force-renewal && \
        cp /home/cert_bot_default.conf /etc/nginx/conf.d/default.conf && \
        nginx -s reload"
    fi
else
    docker exec tg_chat_mate-nginx-service-1 /bin/bash -c "\
    sed -i 's/SERVER_IP_PLACEHOLDER/$DOMAIN/g' /home/conf_without_ssl.conf && \
    cp /home/conf_without_ssl.conf /etc/nginx/conf.d/default.conf && \
    nginx -s reload"
fi

docker compose restart bot