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
echo "ISSUE_SSL: $ISSUE_SSL"

if [[ "$ISSUE_SSL" == "true" ]]; then
    if [[ $DOMAIN =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        docker exec tg_chat_mate-nginx-service-1 /bin/bash -c "\
        apt-get update && apt-get install -y openssl && \
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj '/C=US/ST=New York/L=New York/O=Bouncy Castles, Inc./OU=Ministry of Water/CN=$DOMAIN/emailAddress=admin@your_domain.com' && \
        openssl dhparam -out /etc/nginx/dhparam.pem 2048 && \
        cp /home/self-signed.conf /etc/nginx/snippets/ && \
        cp /home/ssl-params.conf /etc/nginx/snippets/ && \
        cp /home/self_signed.conf /etc/nginx/conf.d/default.conf && \
        cp /etc/ssl/certs/nginx-selfsigned.crt /nginx-certs/ && \
        cp /etc/ssl/private/nginx-selfsigned.key /nginx-certs/ && \
        nginx -s reload "
        docker compose restart bot
    else
        docker exec tg_chat_mate-nginx-service-1 /bin/bash -c "apt-get update && apt-get install -y python3 && \
        apt-get install -y certbot python3-certbot-nginx && \
        cp /home/cert_bot_base.conf /etc/nginx/conf.d/default.conf && \
        certbot --nginx -d $DOMAIN --register-unsafely-without-email --agree-tos --no-eff-email --force-renewal && \
        cp /home/cert_bot_default.conf /etc/nginx/conf.d/default.conf && \
        nginx -s reload"
        docker compose restart bot
    fi
else
    echo ""
fi
