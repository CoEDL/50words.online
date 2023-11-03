FROM nginx:latest
LABEL org.opencontainers.image.source=https://github.com/CoEDL/50words.online
LABEL org.opencontainers.image.description="The 50 words application"
LABEL org.opencontainers.image.licenses=GPLv3

# RUN apt-get update && apt-get install -y nginx-extras
RUN rm /etc/nginx/conf.d/default.conf

COPY ./dist/ /srv/50words/www/

CMD ["nginx", "-g", "daemon off;"]