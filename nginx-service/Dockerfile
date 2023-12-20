FROM nginx:1.24

COPY . /home/

ARG DOMAIN


RUN mkdir -p /etc/nginx/snippets /etc/ssl/private /nginx-certs && \
    mkdir -p /nginx-certs/$DOMAIN && \
    sed -i "s/SERVER_IP_PLACEHOLDER/$DOMAIN/g" /home/self_signed.conf && \
    sed -i "s/SERVER_IP_PLACEHOLDER/$DOMAIN/g" /home/cert_bot_base.conf && \
    sed -i "s/SERVER_IP_PLACEHOLDER/$DOMAIN/g" /home/cert_bot_default.conf && \
    sed -i "s/SERVER_IP_PLACEHOLDER/$DOMAIN/g" /home/conf_without_ssl.conf && \
    cp /home/conf_without_ssl.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
