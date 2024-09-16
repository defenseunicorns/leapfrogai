FROM node:18-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache libreoffice openjdk11-jre fontconfig msttcorefonts-installer \
    && update-ms-fonts \
    && fc-cache -f

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH=${JAVA_HOME}/bin:$PATH

WORKDIR /app

COPY . .

RUN npm ci

ENV NODE_ENV=production
RUN npm run build && npm prune

# Disable request size limit
ENV BODY_SIZE_LIMIT=Infinity \
    PROTOCOL_HEADER=x-forwarded-proto \
    HOST_HEADER=x-forwarded-host

EXPOSE 3000

CMD ["build"]
