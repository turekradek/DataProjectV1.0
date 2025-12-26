# Stage 1: Build stage
FROM python:3.12-slim AS builder
RUN apt-get update && \
    apt-get install -y vim postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: Final stage
FROM python:3.12-slim
COPY --from=builder /usr/bin/vim /usr/bin/vim
COPY --from=builder /usr/bin/psql /usr/bin/psql
