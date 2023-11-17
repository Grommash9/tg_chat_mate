docker-compose down
docker volume prune -f
docker system prune -af
echo "Docker cleanup complete."
git pull
docker compose up -d

set -a
source .env
set +a


if [[ $SERVER_IP_ADDRESS =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "ip conf from sh skipped"
else
    docker exec anonymous_support_bot-nginx-service-1 /bin/bash -c "apt-get update && apt-get install -y python3 && \
    apt-get install -y certbot python3-certbot-nginx && \
    sed -i \"s/SERVER_IP_PLACEHOLDER/$SERVER_IP_ADDRESS/g\" /home/cert_bot_base.conf && \
    sed -i \"s/SERVER_IP_PLACEHOLDER/$SERVER_IP_ADDRESS/g\" /home/cert_bot_default.conf && \
    cp /home/cert_bot_base.conf /etc/nginx/conf.d/default.conf && \
    certbot --nginx -d $SERVER_IP_ADDRESS --register-unsafely-without-email --agree-tos --no-eff-email --force-renewal && \
    cp /home/cert_bot_default.conf /etc/nginx/conf.d/default.conf && \
    nginx -s reload "

fi

