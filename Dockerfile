# syntax=docker/dockerfile:1

# Stage 1: build the application bundle with Node 24
FROM node:24-slim AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npx webpack --config webpack-production.js

# Stage 2: serve the built bundle with nginx
FROM nginx:latest
LABEL org.opencontainers.image.source=https://github.com/CoEDL/50words.online
LABEL org.opencontainers.image.description="The 50 words application"
LABEL org.opencontainers.image.licenses=GPLv3

RUN rm /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist/ /srv/50words/www/

CMD ["nginx", "-g", "daemon off;"]
