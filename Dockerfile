FROM nginx:1.15.2-alpine

RUN rm -rf /etc/nginx/conf.d/*
COPY 50words.online.nginx.conf /etc/nginx/conf.d

EXPOSE 80