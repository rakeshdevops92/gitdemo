# Ubuntu with curl installed
FROM ubuntu:18.04

ENV NGINX_VERSION 1.14.0-0ubuntu1.9
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nginx=$NGINX_VERSION
COPY index.html /var/www/html
ADD https://raw.githubusercontent.com/rakeshdevops92/gitdemo/main/add.html /var/www/html

CMD ["nginx", "-g", "daemon off;"]
