# Multi-stage Dockerfile for React + Bun + Vite Frontend

# Stage 1: Build static assets using Bun
FROM oven/bun:1 AS builder
WORKDIR /app

# Copy package files and install dependencies
COPY frontend/package.json ./
RUN bun install

# Copy source files and build for production
COPY frontend/ ./
RUN bun run build

# Stage 2: Serve built static files using Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
