FROM node:18-alpine AS builder
RUN apk update && apk upgrade && apk add --no-cache libreoffice openjdk11-jre
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH=${JAVA_HOME}/bin:$PATH

WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm ci
COPY . .
ENV NODE_ENV=production
RUN npm run build
RUN npm prune

ENV NODE_ENV=production
# Disable request size limit
ENV BODY_SIZE_LIMIT=Infinity
ENV PROTOCOL_HEADER=x-forwarded-proto
ENV HOST_HEADER=x-forwarded-host
EXPOSE 3000

CMD ["build"]