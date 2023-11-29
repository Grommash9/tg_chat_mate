FROM nginx:1.24

COPY . /home/

ARG DOMAIN

COPY setup.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/setup.sh && /usr/local/bin/setup.sh

CMD ["nginx", "-g", "daemon off;"]
