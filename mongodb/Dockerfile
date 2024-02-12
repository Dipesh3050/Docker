#Dockerfile

FROM mongo:latest

# Install MongoDB tools
RUN apt-get update \
    && apt-get install -y \
        mongodb-clients \
    && rm -rf /var/lib/apt/lists/*