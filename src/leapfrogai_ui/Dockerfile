FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm ci
COPY . .
ENV NODE_ENV=production
RUN cp .env.public .env
RUN npm run build
RUN npm prune

FROM cgr.dev/chainguard/node:latest

WORKDIR /app
COPY --chown=node:node --from=builder /app/build build/
COPY --chown=node:node --from=builder /app/node_modules node_modules/
COPY --chown=node:node package.json .
EXPOSE 3000
ENV NODE_ENV=production
# Disable request size limit
ENV BODY_SIZE_LIMIT=Infinity
ENV PROTOCOL_HEADER=x-forwarded-proto
ENV HOST_HEADER=x-forwarded-host
CMD ["build"]